from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import logging
import os
from .models import Product, Category, ProductImage
import cloudinary.uploader

# 設置日誌
logger = logging.getLogger(__name__)

def home(request):
    featured_products = Product.objects.filter(discount_price__isnull=False)[:3]
    return render(request, 'store/home.html', {'featured_products': featured_products})

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)  # 每頁12個產品
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/product_list.html', {'page_obj': page_obj})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    logger.debug(f'Product {product.name}: cover_image={product.cover_image}, cloudinary_url={product.cloudinary_url}')
    logger.debug(f'Images: {[(img.image, img.cloudinary_url, img.description) for img in images]}')
    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

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

def share_images(request):
    products = Product.objects.filter(cloudinary_url__isnull=False)
    product_images = ProductImage.objects.filter(cloudinary_url__isnull=False)
    return render(request, 'store/share_images.html', {
        'products': products,
        'product_images': product_images
    })

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
                # 儲存至本地
                product_image = ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    description=description
                )
                logger.info(f'Saved local image for product {product.name}: {product_image.image.url}')
                # 上傳至 Cloudinary
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
                return redirect('share_images')
            except Exception as e:
                logger.error(f'Image upload failed: {str(e)}')
                messages.error(request, f'上傳失敗：{str(e)}')
    products = Product.objects.all()
    return render(request, 'store/upload_image.html', {'products': products})