from datetime import timedelta
from django.utils import timezone

from .models import LoyaltyCard, WalletTransaction, Order


# =====================
# CYCLE CHECK
# =====================

def check_and_reset_cycle(card: LoyaltyCard):
    """
    Agar cycle tugagan bo‘lsa:
    - Qolgan bonuslarni expire qiladi
    - Yangi cycle boshlaydi
    """
    if timezone.now() > card.cycle_end:
        if card.current_balance > 0:
            WalletTransaction.objects.create(
                user=card.user,
                amount=-card.current_balance,
                type='expire'
            )

        now = timezone.now()
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

def add_bonus(user, amount: int, reference_id: str | None = None):
    """
    Bonus qo‘shish
    """
    card = user.loyalty_card
    check_and_reset_cycle(card)

    card.current_balance += amount
    card.save(update_fields=["current_balance"])

    WalletTransaction.objects.create(
        user=user,
        amount=amount,
        type='loyalty',
        reference_id=reference_id
    )


# =====================
# SPEND BONUS
# =====================

def spend_bonus(user, amount: int):
    """
    Bonus ishlatish
    """
    card = user.loyalty_card
    check_and_reset_cycle(card)

    if card.current_balance < amount:
        raise ValueError("Bonus yetarli emas")

    card.current_balance -= amount
    card.save(update_fields=["current_balance"])

    WalletTransaction.objects.create(
        user=user,
        amount=-amount,
        type='spend'
    )


# =====================
# PROCESS ORDER
# =====================

def process_order(user, total_amount: float, bonus_amount: int):
    """
    Order yaratadi va bonus qo‘shadi
    """
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
