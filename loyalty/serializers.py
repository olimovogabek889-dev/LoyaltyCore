from rest_framework import serializers
from .models import LoyaltyCard, WalletTransaction


# =========================
# LOYALTY CARD
# =========================

class LoyaltyCardSerializer(serializers.ModelSerializer):
    """
    Loyalty card ma'lumotlari (faqat o‘qish uchun)
    """

    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True
    )

    class Meta:
        model = LoyaltyCard
        fields = [
            "id",
            "user_id",
            "current_balance",
            "cycle_start",
            "cycle_end",
            "cycle_days",
            "cycle_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


# =========================
# WALLET TRANSACTION
# =========================

class WalletTransactionSerializer(serializers.ModelSerializer):
    """
    Wallet transaction tarixi
    """

    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True
    )

    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "user_id",
            "amount",
            "type",
            "reference_id",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "created_at",
        ]


# =========================
# SWAGGER UCHUN REQUEST BODY
# =========================

class BonusAmountSerializer(serializers.Serializer):
    """
    Bonus qo‘shish / ishlatish uchun
    """
    amount = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    """
    Order yaratish uchun
    """
    total_amount = serializers.IntegerField(min_value=1)
    bonus_amount = serializers.IntegerField(min_value=0)
