from store.models import Product, ProductImage

def restore_local_paths():
    for product in Product.objects.all():
        if product.cover_image:
            # 假設public_id為products/covers/og_c，轉為本地路徑
            filename = f"{product.cover_image}.jpg"  # 根據實際副檔名調整
            product.cover_image = f"products/covers/{filename}"
            product.save()
    for image in ProductImage.objects.all():
        if image.image:
            filename = f"{image.image}.jpg"
            image.image = f"products/images/{filename}"
            image.save()
    print("Local paths restored!")

if __name__ == "__main__":
    restore_local_paths()
