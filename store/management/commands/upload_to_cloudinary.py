import os
from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary.uploader
from store.models import Product, ProductImage

class Command(BaseCommand):
    help = 'Upload local images from Product and ProductImage models to Cloudinary'

    def handle(self, *args, **kwargs):
        # 處理 Product.cover_image
        for product in Product.objects.filter(cover_image__isnull=False):
            local_path = os.path.join(settings.MEDIA_ROOT, str(product.cover_image))
            if os.path.exists(local_path):
                try:
                    result = cloudinary.uploader.upload(
                        local_path,
                        folder='gundam_store/covers',
                        resource_type='image',
                        public_id=os.path.splitext(os.path.basename(local_path))[0]
                    )
                    product.cloudinary_url = result['secure_url']
                    product.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'Uploaded cover: {product.name} to {result["secure_url"]}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Failed to upload cover {product.name}: {str(e)}'
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Cover file not found: {local_path}'
                ))

        # 處理 ProductImage.image
        for image in ProductImage.objects.filter(image__isnull=False):
            local_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
            if os.path.exists(local_path):
                try:
                    result = cloudinary.uploader.upload(
                        local_path,
                        folder='gundam_store/images',
                        resource_type='image',
                        public_id=os.path.splitext(os.path.basename(local_path))[0]
                    )
                    image.cloudinary_url = result['secure_url']
                    image.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'Uploaded image: {image} to {result["secure_url"]}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Failed to upload image {image}: {str(e)}'
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Image file not found: {local_path}'
                ))