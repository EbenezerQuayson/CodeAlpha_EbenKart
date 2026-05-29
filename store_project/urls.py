# store_project/urls.py
from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('register/', catalog_views.register, name='register'),
    path('profile/', catalog_views.profile_view, name='profile_view'),
    path('cart/', include('cart.urls')),
    path('products/', catalog_views.shop_home, name='shop_home'),
    path('products/<int:product_id>/', catalog_views.product_detail, name='product_detail'),
    path('categories/', catalog_views.categories_view, name='categories_view'),
    path('contact/', catalog_views.contact_view, name='contact_view'),
    
    # Add the home route here:
    path('', catalog_views.store_home, name='home'),
]