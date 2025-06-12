# store/management/commands/check_images.py
from django.core.management.base import BaseCommand
from store.models import Product, ProductImage
import os

class Command(BaseCommand):
    help = '檢查圖片記錄與檔案狀態'

    def handle(self, *args, **kwargs):
        self.stdout.write("檢查 Product 圖片...")
        for p in Product.objects.all():
            status = os.path.exists(p.cover_image.path) if p.cover_image else "無檔案"
            self.stdout.write(f"{p.name}: cover_image={p.cover_image}, exists={status}, cloudinary_url={p.cloudinary_url}")

        self.stdout.write("\n檢查 ProductImage 圖片...")
        for i in ProductImage.objects.all():
            status = os.path.exists(i.image.path) if i.image else "無檔案"
            self.stdout.write(f"{i.product.name} #{i.id}: image={i.image}, exists={status}, cloudinary_url={i.cloudinary_url}")