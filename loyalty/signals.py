from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import LoyaltyCard


@receiver(post_save, sender=User)
def create_loyalty_card(sender, instance, created, **kwargs):
    if created:
        now = timezone.now()
        LoyaltyCard.objects.create(
            user=instance,
            current_balance=0,
            cycle_start=now,
            cycle_end=now + timedelta(days=60),
            cycle_days=60,
            cycle_number=1,
        )
