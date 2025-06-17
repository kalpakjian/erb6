import random
from django.core.management.base import BaseCommand
from store.models import Product  # 假設 Product 模型在 store.models 中

class Command(BaseCommand):
    help = '檢查產品 scale 值，若不存在或為空，隨機賦予 RG, HG, MG, PG 中的一個值'

    def handle(self, *args, **kwargs):
        valid_scales = ['RG', 'HG', 'MG', 'PG']
        products = Product.objects.all()
        updated_count = 0

        for product in products:
            if not product.scale or product.scale.strip() == '':
                product.scale = random.choice(valid_scales)
                product.save()
                updated_count += 1
                self.stdout.write(f'已更新產品 {product.name} 的 scale 為 {product.scale}')

        self.stdout.write(self.style.SUCCESS(f'完成！共更新 {updated_count} 個產品的 scale 值。'))