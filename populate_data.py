from django.contrib.auth.models import User
from store.models import Category, Product, ProductImage
from django.utils import timezone
from pathlib import Path
import os

def populate():
    # Clear existing data (optional)
    ProductImage.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()

    # Create categories
    wing = Category.objects.create(name="Gundam Wing", description="Models from Gundam Wing series")
    seed = Category.objects.create(name="Gundam Seed", description="Models from Gundam Seed series")

    # Create products
    products = [
        {
            "name": "Gundam Wing Zero",
            "description": "Iconic Wing Zero model with twin buster rifle.",
            "price": 1200.00,
            "discount_price": 1000.00,
            "stock": 50,
            "category": wing,
            "scale": "1/144",
            "images": [],
        },
        {
            "name": "Gundam Destiny",
            "description": "High-performance model from Gundam Seed Destiny.",
            "price": 1500.00,
            "discount_price": 1300.00,
            "stock": 30,
            "category": seed,
            "scale": "1/100",
            "images": [],
        },
        {
            "name": "Gundam Strike Freedom",
            "description": "Advanced model with DRAGOON system.",
            "price": 1800.00,
            "discount_price": None,
            "stock": 20,
            "category": seed,
            "scale": "1/100",
            "images": [],
        },
        {
            "name": "Gundam Sandrock",
            "description": "Heavy-armored model from Gundam Wing.",
            "price": 1000.00,
            "discount_price": 900.00,
            "stock": 40,
            "category": wing,
            "scale": "1/144",
            "images": [],
        },
    ]

    for product_data in products:
        product = Product.objects.create(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            discount_price=product_data["discount_price"],
            stock=product_data["stock"],
            category=product_data["category"],
            scale=product_data["scale"],
            created_at=timezone.now(),
        )
        for img in product_data["images"]:
            # Note: Ensure image files exist at specified paths
            ProductImage.objects.create(
                product=product,
                image=img["path"],
                description=img["description"],
                order=0,
            )

if __name__ == "__main__":
    print("Populating test data...")
    populate()
    print("Done!")