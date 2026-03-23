from django.contrib import admin
from .models import Supply, SupplyProduct

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'storage', 'delivery_date')
    list_filter = ('supplier',)

@admin.register(SupplyProduct)
class SupplyProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'supply', 'product', 'quantity')
    list_filter = ('supply',)
