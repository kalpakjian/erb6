from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    featured_products = Product.objects.filter(discount_price__isnull=False)[:3]
    return render(request, 'store/home.html', {'featured_products': featured_products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})