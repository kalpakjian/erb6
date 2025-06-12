"""
store/views.py
Django views for gundam_store project.
"""

import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage, Cart, CartItem, Order, OrderItem
import cloudinary.uploader

# 設置日誌
logger = logging.getLogger(__name__)

# 首頁
def home(request):
    featured_products = Product.objects.filter(discount_price__isnull=False)[:3]
    return render(request, 'store/home.html', {'featured_products': featured_products})

# 產品列表
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/product_list.html', {'page_obj': page_obj})

# 產品詳情
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    logger.debug(f'Product {product.name}: cover_image={product.cover_image}, cloudinary_url={product.cloudinary_url}')
    logger.debug(f'Images: {[(img.image, img.cloudinary_url, img.description) for img in images]}')
    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images
    })

# 分類列表
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

# 分類詳情
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'page_obj': page_obj
    })

# 產品搜尋
def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/search_results.html', {
        'page_obj': page_obj,
        'query': query
    })

# 圖片分享
def share_images(request):
    products = Product.objects.filter(cloudinary_url__isnull=False)
    product_images = ProductImage.objects.filter(cloudinary_url__isnull=False)
    return render(request, 'store/share_images.html', {
        'products': products,
        'product_images': product_images
    })

# 上傳圖片
# store/views.py
def upload_image(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        image_file = request.FILES.get('image')
        description = request.POST.get('description', '')
        if not product_id:
            messages.error(request, '請選擇產品！')
        elif not image_file:
            messages.error(request, '請選擇圖片檔案！')
        elif not image_file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            messages.error(request, '僅支援 JPG 或 PNG 格式！')
        elif image_file.size > 10 * 1024 * 1024:  # 10MB
            messages.error(request, '檔案大小不得超過 10MB！')
        else:
            try:
                product = get_object_or_404(Product, id=product_id)
                product_image = ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    description=description
                )
                logger.info(f'Saved local image for product {product.name}: {product_image.image.url}')
                result = cloudinary.uploader.upload(
                    product_image.image.path,
                    folder='gundam_store/images',
                    resource_type='image',
                    public_id=f"{product.name}_{os.path.splitext(image_file.name)[0]}",
                    quality='auto'
                )
                product_image.cloudinary_url = result['secure_url']
                product_image.save()
                logger.info(f'Uploaded image to Cloudinary for product {product.name}: {result["secure_url"]}')
                messages.success(request, '圖片上傳成功！')
                return redirect('store:share_images')  # 修正
            except Exception as e:
                logger.error(f'Image upload failed: {str(e)}')
                messages.error(request, f'上傳失敗：{str(e)}')
    products = Product.objects.all()
    return render(request, 'store/upload_image.html', {'products': products})

# 購物車
def cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        session_key=session_key
    )
    return render(request, 'store/cart.html', {'cart': cart})

# 結帳
def checkout(request):
    session_key = request.session.session_key
    cart = get_object_or_404(Cart, user=request.user if request.user.is_authenticated else None, session_key=session_key)
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            messages.error(request, '請輸入送貨地址！')
        elif not cart.items.exists():
            messages.error(request, '購物車為空！')
        else:
            total_price = sum(item.product.price * item.quantity for item in cart.items.all())
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=session_key,
                shipping_address=shipping_address,
                total_price=total_price,
                status='pending'
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.items.all().delete()
            messages.success(request, '訂單已提交！')
            return redirect('store:orders')
    return render(request, 'store/checkout.html', {'cart': cart})

# 用戶註冊
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功，請登入！')
            return redirect('store:login')
        else:
            messages.error(request, '註冊失敗，請檢查表單！')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# 用戶個人資料
@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        messages.success(request, '個人資料已更新！')
        return redirect('store:profile')
    return render(request, 'store/profile.html', {'user': request.user})

# 訂單歷史
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})