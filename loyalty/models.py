from django.db import models
from django.contrib.auth.models import User


class LoyaltyCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(default=0)

    cycle_start = models.DateTimeField()
    cycle_end = models.DateTimeField()
    cycle_days = models.IntegerField(default=60)
    cycle_number = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LoyaltyCard(user={self.user_id}, balance={self.current_balance})"


class WalletTransaction(models.Model):
    TYPE_CHOICES = (
        ('loyalty', 'Loyalty'),
        ('referral', 'Referral'),
        ('milestone', 'Milestone'),
        ('spend', 'Spend'),
        ('expire', 'Expire'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reference_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} {self.amount} (user={self.user_id})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - User {self.user_id}"
