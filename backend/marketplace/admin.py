from django.contrib import admin
from .models import Product, ProductImage, Enquiry


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price', 'location', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'location', 'seller__email']
    inlines = [ProductImageInline]


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['product__name', 'buyer__email', 'message']