from django.db import models
from company.models import Company

class Storage(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='storages'
    )
    address = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.company.title_company} - {self.address}"
