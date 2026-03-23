from django.db import models
from storage.models import Storage

class Product(models.Model):
    title = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='products'
    )
    description = models.CharField(max_length=100, blank=True, null=True)
