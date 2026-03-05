from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Company

class User(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_company_owner = models.BooleanField(default=False)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
