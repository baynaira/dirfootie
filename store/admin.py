from django.contrib import admin
from .models import Category, Product
from .order_models import Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
