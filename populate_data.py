from django.contrib.auth.models import User
from store.models import Category, Product, ProductImage
from django.utils import timezone
from pathlib import Path
import os

def populate_customers():
    # Clear existing users (optional, be cautious in production)
    User.objects.filter(is_superuser=False).delete()

    # Create customers
    customers = [
        {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
        },
        {
            "username": "jane_smith",
            "email": "jane.smith@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "password": "password123",
        },
        {
            "username": "alex_wong",
            "email": "alex.wong@example.com",
            "first_name": "Alex",
            "last_name": "Wong",
            "password": "password123",
        },
    ]

    for customer in customers:
        User.objects.create_user(
            username=customer["username"],
            email=customer["email"],
            first_name=customer["first_name"],
            last_name=customer["last_name"],
            password=customer["password"],
        )

if __name__ == "__main__":
    print("Populating customer data...")
    populate_customers()
    print("Done!")