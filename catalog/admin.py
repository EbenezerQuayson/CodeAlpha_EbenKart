from django.contrib import admin
from .models import Product, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'country', 'payment_method')
    search_fields = ('user__username', 'phone_number', 'city', 'country')
    list_filter = ('payment_method', 'country')

