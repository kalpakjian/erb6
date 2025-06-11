import os
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Product, ProductImage, Category

class Command(BaseCommand):
    help = 'Import local images from media folder into Product and ProductImage models'

    def handle(self, *args, **kwargs):
        # 創建一個臨時分類（若無分類）
        category, _ = Category.objects.get_or_create(
            name='Temporary',
            defaults={'description': 'Temporary category for imported images'}
        )

        # 處理 covers 資料夾（Product.cover_image）
        covers_path = os.path.join(settings.MEDIA_ROOT, 'products', 'covers')
        for filename in os.listdir(covers_path):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                file_path = os.path.join('products', 'covers', filename)
                if not Product.objects.filter(cover_image=file_path).exists():
                    # 創建臨時產品
                    product_name = os.path.splitext(filename)[0]
                    product = Product.objects.create(
                        name=product_name,
                        description=f'Imported product for {filename}',
                        price=0.00,
                        stock=0,
                        category=category,
                        cover_image=file_path
                    )
                    self.stdout.write(self.style.SUCCESS(f'Imported cover: {filename} for product {product_name}'))

        # 處理 images 資料夾（ProductImage.image）
        images_path = os.path.join(settings.MEDIA_ROOT, 'products', 'images')
        for filename in os.listdir(images_path):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                file_path = os.path.join('products', 'images', filename)
                if not ProductImage.objects.filter(image=file_path).exists():
                    # 假設圖片名稱與產品名稱相關，嘗試匹配
                    product_name = os.path.splitext(filename)[0].split('_')[0]  # 例如 '0g_02' -> '0g'
                    product = Product.objects.filter(name__icontains=product_name).first()
                    if not product:
                        # 創建臨時產品
                        product = Product.objects.create(
                            name=product_name,
                            description=f'Imported product for {filename}',
                            price=0.00,
                            stock=0,
                            category=category
                        )
                    ProductImage.objects.create(
                        product=product,
                        image=file_path,
                        description=f'Imported image {filename}'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Imported image: {filename} for product {product.name}'))