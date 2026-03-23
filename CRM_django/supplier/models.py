from django.db import models
from company.models import Company

class Supplier(models.Model):
    inn_supplier = models.CharField(max_length=12, unique=True, blank=True)
    title = models.CharField(max_length=50, unique=True, blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='suppliers'
    )

