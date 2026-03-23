from django.db import models
from storage.models import Storage
from supplier.models import Supplier
from product.models import Product
from django.utils import timezone


class Supply(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='supplies'
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='supplies'
    )
    delivery_date = models.DateTimeField(default=timezone.now)
    products = models.ManyToManyField(
        Product,
        through='SupplyProduct',
        related_name='supplies'
    )

class SupplyProduct(models.Model):
    supply = models.ForeignKey(
        Supply,
        on_delete=models.CASCADE,
        related_name='supply_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='supply_products'
    )
    quantity = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        product = self.product

        if not self.pk:
            product.quantity += self.quantity
            product.save()

        super().save(*args, **kwargs)
