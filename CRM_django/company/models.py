from django.db import models
from django.conf import settings

class Company(models.Model):
    inn_company = models.CharField(max_length=12, unique=True, null=True)
    title_company = models.CharField(max_length=50, unique=True, null=True)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_company',
        null=True
    )

    def __str__(self):
        return self.title_company
