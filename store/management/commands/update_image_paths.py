from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = '更新 Cloudinary 的 cover_image 路徑'

    def handle(self, *args, **kwargs):
        for product in Product.objects.all():
            if product.cover_image and 'media/' in str(product.cover_image):
                new_path = str(product.cover_image).replace('media/', '')
                product.cover_image = new_path
                product.save()
                self.stdout.write(self.style.SUCCESS(f'已更新 {product.name}'))