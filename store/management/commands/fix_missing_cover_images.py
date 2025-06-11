import os
from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary.uploader
from store.models import Product

class Command(BaseCommand):
    help = '為缺少 cloudinary_url 的 Product 上傳封面圖片'

    def handle(self, *args, **kwargs):
        products = Product.objects.filter(cloudinary_url__isnull=True, cover_image__isnull=False)
        for product in products:
            local_path = os.path.join(settings.MEDIA_ROOT, str(product.cover_image))
            if os.path.exists(local_path):
                try:
                    result = cloudinary.uploader.upload(
                        local_path,
                        folder='gundam_store/covers',
                        resource_type='image',
                        public_id=f"{product.name}_{os.path.splitext(os.path.basename(local_path))[0]}",
                        quality='auto'
                    )
                    product.cloudinary_url = result['secure_url']
                    product.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'成功上傳封面圖片: {product.name} 至 {result["secure_url"]}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'上傳封面圖片 {product.name} 失敗: {str(e)}'
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'找不到封面圖片檔案: {local_path}'
                ))