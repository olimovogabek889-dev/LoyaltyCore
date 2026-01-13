from django.utils import timezone
from datetime import timedelta

from .models import WalletTransaction, Order


def check_and_reset_cycle(card):
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
        card.save()


def add_bonus(user, amount, reference_id=None):
    card = user.loyaltycard
    check_and_reset_cycle(card)

    card.current_balance += amount
    card.save()

    WalletTransaction.objects.create(
        user=user,
        amount=amount,
        type='loyalty',
        reference_id=reference_id
    )


def spend_bonus(user, amount):
    card = user.loyaltycard
    check_and_reset_cycle(card)

    if card.current_balance < amount:
        raise ValueError("Bonus yetarli emas")

    card.current_balance -= amount
    card.save()

    WalletTransaction.objects.create(
        user=user,
        amount=-amount,
        type='spend'
    )


def process_order(user, total_amount, bonus_amount):
    """
    Order yaratiladi va bonus avtomatik qo‘shiladi
    Sikl muddati uzaytirilmaydi
    """
    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        bonus_amount=bonus_amount
    )

    add_bonus(
        user=user,
        amount=bonus_amount,
        reference_id=str(order.id)
    )

    return order
from .models import Order
from .services import add_bonus


def process_order(order: Order):
    """
    Order yaratilganda bonus qo‘shadi
    cycle muddatini uzaytirmaydi
    """
    bonus = order.bonus_amount
    if bonus > 0:
        add_bonus(
            user=order.user,
            amount=bonus,
            reference_id=f"order_{order.id}"
        )
