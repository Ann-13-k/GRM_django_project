from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete, sender=Company)
def reset_owner_flag(sender, instance, **kwargs):
    owner = instance.owner

    if owner:
        owner.is_company_owner = False
        owner.company = None
        owner.save()