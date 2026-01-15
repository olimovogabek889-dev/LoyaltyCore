from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# =====================
# LOYALTY CARD
# =====================

class LoyaltyCard(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='loyalty_card'
    )

    current_balance = models.IntegerField(default=0)

    cycle_start = models.DateTimeField(default=timezone.now)
    cycle_days = models.IntegerField(default=60)
    cycle_number = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def cycle_end(self):
        return self.cycle_start + timedelta(days=self.cycle_days)

    def start_new_cycle(self):
        self.cycle_start = timezone.now()
        self.cycle_number += 1
        self.current_balance = 0
        self.save()

    def __str__(self):
        return f"LoyaltyCard(user={self.user.username}, balance={self.current_balance})"


# =====================
# WALLET TRANSACTIONS
# =====================

class WalletTransaction(models.Model):
    TYPE_CHOICES = (
        ('loyalty', 'Loyalty'),
        ('referral', 'Referral'),
        ('milestone', 'Milestone'),
        ('spend', 'Spend'),
        ('expire', 'Expire'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wallet_transactions'
    )

    amount = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reference_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.type} | {self.amount}"


# =====================
# ORDERS
# =====================

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} | {self.user.username}"
