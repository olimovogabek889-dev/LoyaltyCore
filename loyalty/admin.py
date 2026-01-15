from django.contrib import admin
from .models import LoyaltyCard, WalletTransaction, Order


@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'current_balance',
        'cycle_number',
        'cycle_start',
        'cycle_end',
        'created_at',
    )

    list_filter = (
        'cycle_number',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    ordering = (
        '-created_at',
    )


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'type',
        'amount',
        'created_at',
    )

    list_filter = (
        'type',
        'created_at',
    )

    search_fields = (
        'user__username',
    )

    ordering = (
        '-created_at',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'bonus_amount',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'user__username',
    )

    ordering = (
        '-created_at',
    )
