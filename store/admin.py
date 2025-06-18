from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # 預設顯示 1 個圖片上傳欄位

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'stock', 'scale', 'category']
    list_filter = ['category', 'scale']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
    