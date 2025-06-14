# store/urls.py
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # 現有 endpoints
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('search/', views.search_products, name='search_products'),
    path('share/', views.share_images, name='share_images'),
    path('upload/', views.upload_image, name='upload_image'),
    # 購物車與結帳
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # 用戶相關
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.order_history, name='orders'),
]