from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .services import process_order


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        process_order(instance)
