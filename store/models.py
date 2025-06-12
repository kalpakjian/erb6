# store/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    scale = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='products/covers/', blank=True, null=True)
    cloudinary_url = models.URLField(max_length=500, blank=True)

    def get_cover_url(self):
        if self.cloudinary_url:
            return self.cloudinary_url
        elif self.cover_image:
            return self.cover_image.url
        return None

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    cloudinary_url = models.URLField(max_length=500, blank=True)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    def get_image_url(self):
        if self.cloudinary_url:
            return self.cloudinary_url
        elif self.image:
            return self.image.url
        return None

    def __str__(self):
        return f"Image for {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # 支援未登入用戶

    def __str__(self):
        return f"Cart for {self.user or self.session_key}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', '待處理'),
        ('shipped', '已發貨'),
        ('delivered', '已送達'),
        ('cancelled', '已取消'),
    ], default='pending')
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # 支援未登入訂單

    def __str__(self):
        return f"Order {self.id} by {self.user or self.session_key}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 訂單時的價格

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"