from django.contrib import admin
from .models import LoyaltyCard, WalletTransaction


@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'current_balance',
        'cycle_number',
        'cycle_start',
        'cycle_end',
    )


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount',
        'type',
        'created_at',
    )
