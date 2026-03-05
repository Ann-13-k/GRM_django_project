from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "username",
        "is_company_owner",
        "company"
    )

    fieldsets = (
        ("Основная информация", {
            "fields": ("email", "username", "password"),
        }),
        ("Компания", {
            "fields": ("is_company_owner", "company"),
        }),
        ("Права доступа", {
            "fields": ("is_active", "is_staff", "is_superuser"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    ordering = ("email",)


