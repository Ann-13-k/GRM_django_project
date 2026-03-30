from django.db import models
from company.models import Company
from product.models import Product
from django.utils import timezone

class Sale(models.Model):
    buyer_name = models.CharField(max_length=50, blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='sales'
    )

    products = models.ManyToManyField(
        Product,
        through='ProductSale',
        related_name='sales'
    )
    sale_date = models.DateField(default=timezone.now)

class ProductSale(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='product_sales'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_sales'
    )

    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        product = self.product

        if not self.pk:
            if product.quantity < self.quantity:
                raise ValueError("Недостаточно товара на складе")

            product.quantity -= self.quantity
            product.save()

        super().save(*args, **kwargs)

