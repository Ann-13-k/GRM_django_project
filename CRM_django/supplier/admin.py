from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'inn_supplier', 'title', 'company')
    search_fields = ('title', 'inn_supplier')
    list_filter = ('company',)