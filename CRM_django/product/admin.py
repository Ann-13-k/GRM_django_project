from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'quantity', 'purchase_price', 'sale_price', 'storage', 'description')
    list_filter = ('title',)
