from django.core.management.base import BaseCommand
from store.models import Product, ProductImage
import cloudinary.uploader

class Command(BaseCommand):
    help = '檢查並同步本地圖檔至 Cloudinary'

    def handle(self, *args, **kwargs):
        # 同步 Product 的封面圖片
        for product in Product.objects.filter(cloudinary_url__isnull=True, cover_image__isnull=False):
            try:
                result = cloudinary.uploader.upload(
                    product.cover_image.path,
                    folder='gundam_store/covers',
                    resource_type='image',
                    public_id=f"cover_{product.name}",
                    quality='auto'
                )
                product.cloudinary_url = result['secure_url']
                product.save()
                self.stdout.write(self.style.SUCCESS(f'已同步 {product.name} 的封面圖片'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'同步 {product.name} 失敗: {str(e)}'))

        # 同步 ProductImage 的圖片
        for image in ProductImage.objects.filter(cloudinary_url__isnull=True, image__isnull=False):
            try:
                result = cloudinary.uploader.upload(
                    image.image.path,
                    folder='gundam_store/images',
                    resource_type='image',
                    public_id=f"image_{image.product.name}_{image.id}",
                    quality='auto'
                )
                image.cloudinary_url = result['secure_url']
                image.save()
                self.stdout.write(self.style.SUCCESS(f'已同步 {image.product.name} 的圖片 #{image.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'同步 {image.product.name} 圖片 #{image.id} 失敗: {str(e)}'))