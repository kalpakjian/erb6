# store/admin.py
import os
from django.contrib import admin
from django import forms
from django.conf import settings
from .models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'banner_path']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 動態生成 banner_path 選項
        banner_choices = [('', '無')]  # 允許選擇空值
        banner_dir = os.path.join(settings.STATICFILES_DIRS[0], 'banners')
        if os.path.exists(banner_dir):
            for filename in os.listdir(banner_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    banner_path = f'banners/{filename}'
                    banner_choices.append((banner_path, filename))
        self.fields['banner_path'].widget = forms.Select(choices=banner_choices)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # 預設顯示 1 個圖片上傳欄位

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['name', 'description', 'banner_path']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'stock', 'scale', 'category']
    list_filter = ['category', 'scale']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]

#admin.site.register(Cart)
#admin.site.register(CartItem)
#admin.site.register(Order)
#admin.site.register(OrderItem)