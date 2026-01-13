from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from loyalty.models import LoyaltyCard, WalletTransaction


class Command(BaseCommand):
    help = "Reset expired loyalty cycles"

    def handle(self, *args, **options):
        now = timezone.now()
        expired_cards = LoyaltyCard.objects.filter(cycle_end__lt=now)

        count = 0

        for card in expired_cards:
            # Expire remaining balance
            if card.current_balance > 0:
                WalletTransaction.objects.create(
                    user=card.user,
                    amount=-card.current_balance,
                    type='expire'
                )

            # Reset cycle
            card.current_balance = 0
            card.cycle_number += 1
            card.cycle_start = now
            card.cycle_end = now + timedelta(days=card.cycle_days)
            card.save()

            count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{count} loyalty cycles reset successfully")
        )
