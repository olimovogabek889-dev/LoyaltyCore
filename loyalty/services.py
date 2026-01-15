from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from .models import LoyaltyCard, WalletTransaction, Order


# =====================
# CYCLE CHECK
# =====================

def check_and_reset_cycle(card: LoyaltyCard):
    """
    Agar loyalty cycle tugagan bo‘lsa:
    - Qolgan bonuslarni expire qiladi
    - Yangi cycle boshlaydi
    """
    now = timezone.now()

    if now <= card.cycle_end:
        return

    # Eski balansni expire qilish
    if card.current_balance > 0:
        WalletTransaction.objects.create(
            user=card.user,
            amount=-card.current_balance,
            type="expire",
            reference_id=f"cycle_{card.cycle_number}"
        )

    # Yangi cycle
    card.current_balance = 0
    card.cycle_number += 1
    card.cycle_start = now
    card.cycle_end = now + timedelta(days=card.cycle_days)

    card.save(update_fields=[
        "current_balance",
        "cycle_number",
        "cycle_start",
        "cycle_end",
    ])


# =====================
# ADD BONUS
# =====================

@transaction.atomic
def add_bonus(user, amount: int, reference_id: str | None = None):
    """
    Bonus qo‘shish
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")

    try:
        card = user.loyalty_card
    except LoyaltyCard.DoesNotExist:
        raise ValueError("Loyalty card not found")

    check_and_reset_cycle(card)

    card.current_balance += amount
    card.save(update_fields=["current_balance"])

    WalletTransaction.objects.create(
        user=user,
        amount=amount,
        type="loyalty",
        reference_id=reference_id
    )


# =====================
# SPEND BONUS
# =====================

@transaction.atomic
def spend_bonus(user, amount: int):
    """
    Bonus ishlatish
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")

    try:
        card = user.loyalty_card
    except LoyaltyCard.DoesNotExist:
        raise ValueError("Loyalty card not found")

    check_and_reset_cycle(card)

    if card.current_balance < amount:
        raise ValueError("Bonus yetarli emas")

    card.current_balance -= amount
    card.save(update_fields=["current_balance"])

    WalletTransaction.objects.create(
        user=user,
        amount=-amount,
        type="spend"
    )


# =====================
# PROCESS ORDER
# =====================

@transaction.atomic
def process_order(user, total_amount: float, bonus_amount: int):
    """
    Order yaratadi va bonus qo‘shadi
    """
    if total_amount <= 0:
        raise ValueError("Total amount must be positive")

    if bonus_amount < 0:
        raise ValueError("Bonus amount cannot be negative")

    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        bonus_amount=bonus_amount
    )

    if bonus_amount > 0:
        add_bonus(
            user=user,
            amount=bonus_amount,
            reference_id=f"order_{order.id}"
        )

    return order
