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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Product, Category, ProductImage, Cart, CartItem, Order, OrderItem
import cloudinary.uploader

# 設置日誌
logger = logging.getLogger(__name__)

# 首頁
def home(request):
    featured_products = Product.objects.filter(discount_price__isnull=False)[:3]
    context = {
        'featured_products': featured_products,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/home.html', context)

# 產品列表
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/product_list.html', context)

# 產品詳情
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    logger.debug(f'Product {product.name}: cover_image={product.cover_image}, cloudinary_url={product.cloudinary_url}')
    logger.debug(f'Images: {[(img.image, img.cloudinary_url, img.description) for img in images]}')
    context = {
        'product': product,
        'images': images,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/product_detail.html', context)

# 分類列表
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/category_list.html', context)

# 分類詳情
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/category_detail.html', context)

# 產品搜尋
def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'query': query,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/search_results.html', context)

# 圖片分享
def share_images(request):
    products = Product.objects.filter(cloudinary_url__isnull=False)
    product_images = ProductImage.objects.filter(cloudinary_url__isnull=False)
    context = {
        'products': products,
        'product_images': product_images,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/share_images.html', context)

# 上傳圖片
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
                return redirect('store:share_images')
            except Exception as e:
                logger.error(f'Image upload failed: {str(e)}')
                messages.error(request, f'上傳失敗：{str(e)}')
    products = Product.objects.all()
    context = {
        'products': products,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/upload_image.html', context)

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
    context = {
        'cart': cart,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            messages.error(request, '數量必須大於 0！')
            return redirect('store:product_detail', pk=product_id)
        if product.stock < quantity:
            messages.error(request, f'庫存不足，僅剩 {product.stock} 件！')
            return redirect('store:product_detail', pk=product_id)

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key
        )
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, f'已將 {product.name} 添加到購物車！')
    return redirect('store:cart')

def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            cart_item.delete()
            messages.success(request, f'已移除 {cart_item.product.name}！')
        elif cart_item.product.stock < quantity:
            messages.error(request, f'庫存不足，僅剩 {cart_item.product.stock} 件！')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'已更新 {cart_item.product.name} 數量！')
    return redirect('store:cart')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'已移除 {product_name}！')
    return redirect('store:cart')

# 結帳
def checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart = get_object_or_404(Cart, user=request.user if request.user.is_authenticated else None, session_key=session_key)
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            messages.error(request, '請輸入送貨地址！')
            return render(request, 'store/checkout.html', {'cart': cart})
        if not cart.items.exists():
            messages.error(request, '購物車為空！')
            return render(request, 'store/checkout.html', {'cart': cart})
        
        # 檢查庫存
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                messages.error(request, f'{item.product.name} 庫存不足，僅剩 {item.product.stock} 件！')
                return render(request, 'store/checkout.html', {'cart': cart})

        # 計算總價（考慮折扣價）
        total_price = sum(item.get_subtotal() for item in cart.items.all())
        
        # 創建訂單
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            shipping_address=shipping_address,
            total_price=total_price,
            status='pending'
        )
        
        # 創建訂單項目並更新庫存
        for item in cart.items.all():
            price = item.product.discount_price if item.product.discount_price else item.product.price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=price
            )
            item.product.stock -= item.quantity
            item.product.save()
        
        # 清空購物車
        cart.items.all().delete()
        messages.success(request, '訂單已提交！')
        return redirect('store:orders')
    
    context = {
        'cart': cart,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/checkout.html', context)

# 用戶個人資料
@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        messages.success(request, '個人資料已更新！')
        return redirect('store:profile')
    context = {
        'user': request.user,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/profile.html', context)

# 訂單歷史
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }
    return render(request, 'store/orders.html', context)