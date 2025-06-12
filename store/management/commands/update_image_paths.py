from django.core.management.base import BaseCommand
from store.models import Product, ProductImage
import cloudinary.uploader
import os
from django.db.models import Q

class Command(BaseCommand):
    help = '檢查並同步本地圖檔至 Cloudinary'

    def handle(self, *args, **kwargs):
        self.stdout.write("開始同步圖片至 Cloudinary...")

        # 檢查待同步的記錄（兼容 cloudinary_url 為空字串或 NULL）
        product_count = Product.objects.filter(Q(cloudinary_url__isnull=True) | Q(cloudinary_url=''), cover_image__isnull=False).count()
        image_count = ProductImage.objects.filter(Q(cloudinary_url__isnull=True) | Q(cloudinary_url=''), image__isnull=False).count()
        self.stdout.write(f"待同步的 Product 數量: {product_count}")
        self.stdout.write(f"待同步的 ProductImage 數量: {image_count}")

        # 同步 Product 的封面圖片
        processed_products = 0
        for product in Product.objects.filter(Q(cloudinary_url__isnull=True) | Q(cloudinary_url=''), cover_image__isnull=False):
            try:
                if not os.path.exists(product.cover_image.path):
                    self.stdout.write(self.style.WARNING(f'圖片檔案不存在: {product.cover_image.path}'))
                    continue
                result = cloudinary.uploader.upload(
                    product.cover_image.path,
                    folder='gundam_store/covers',
                    resource_type='image',
                    public_id=f"cover_{product.name}",
                    quality='auto'
                )
                product.cloudinary_url = result['secure_url']
                product.save()
                processed_products += 1
                self.stdout.write(self.style.SUCCESS(f'已同步 {product.name} 的封面圖片: {result["secure_url"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'同步 {product.name} 失敗: {str(e)}'))

        # 同步 ProductImage 的圖片
        processed_images = 0
        for image in ProductImage.objects.filter(Q(cloudinary_url__isnull=True) | Q(cloudinary_url=''), image__isnull=False):
            try:
                if not os.path.exists(image.image.path):
                    self.stdout.write(self.style.WARNING(f'圖片檔案不存在: {image.image.path}'))
                    continue
                result = cloudinary.uploader.upload(
                    image.image.path,
                    folder='gundam_store/images',
                    resource_type='image',
                    public_id=f"image_{image.product.name}_{image.id}",
                    quality='auto'
                )
                image.cloudinary_url = result['secure_url']
                image.save()
                processed_images += 1
                self.stdout.write(self.style.SUCCESS(f'已同步 {image.product.name} 的圖片 #{image.id}: {result["secure_url"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'同步 {image.product.name} 圖片 #{image.id} 失敗: {str(e)}'))

        # 總結
        self.stdout.write(f"同步完成！處理的 Product 數量: {processed_products}, ProductImage 數量: {processed_images}")
        if processed_products + processed_images == 0:
            self.stdout.write(self.style.WARNING("無圖片需要同步，可能無待處理記錄或圖片檔案缺失。"))