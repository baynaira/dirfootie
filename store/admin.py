from django.contrib import admin
from .models import Category, Product, ProductImage
from .order_models import Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Allows you to add one additional image at a time

# Customize the Product admin to include the inline
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
