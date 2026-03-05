from django.contrib import admin
from . import models

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["inn_company", "title_company"]
