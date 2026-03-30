from django.contrib import admin
from .models import Sale, ProductSale

class ProductSaleInline(admin.TabularInline):
    model = ProductSale
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_name', 'company', 'sale_date')
    list_filter = ('company',)
    inlines = [ProductSaleInline]

@admin.register(ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'quantity')
    list_filter = ('sale', 'product')

