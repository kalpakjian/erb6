import os
from django.conf import settings
from store.models import Product, ProductImage
import cloudinary.uploader

def migrate_images():
    # 遍歷所有產品
    for product in Product.objects.all():
        if product.cover_image and os.path.exists(product.cover_image.path):
            print(f"Uploading cover image for {product.name}")
            result = cloudinary.uploader.upload(
                product.cover_image.path,
                folder=f"products/covers/",
                public_id=os.path.splitext(os.path.basename(product.cover_image.name))[0]
            )
            product.cover_image = result['public_id']
            product.save()

    # 遍歷所有實物圖片
    for image in ProductImage.objects.all():
        if image.image and os.path.exists(image.image.path):
            print(f"Uploading image for {image.product.name}")
            result = cloudinary.uploader.upload(
                image.image.path,
                folder=f"products/images/",
                public_id=os.path.splitext(os.path.basename(image.image.name))[0]
            )
            image.image = result['public_id']
            image.save()

    print("Migration completed!")

if __name__ == "__main__":
    migrate_images()
