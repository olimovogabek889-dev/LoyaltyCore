from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .serializers import (
    LoyaltyCardSerializer,
    WalletTransactionSerializer,
    BonusAmountSerializer,
    CreateOrderSerializer,
)
from .services import (
    add_bonus,
    spend_bonus,
    process_order,
)


# =====================
# LOYALTY CARD
# =====================

class LoyaltyCardView(APIView):
    """
    GET:
    - Foydalanuvchining loyalty card ma'lumotlarini qaytaradi
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=LoyaltyCardSerializer,
        tags=["Loyalty"]
    )
    def get(self, request):
        try:
            card = request.user.loyalty_card
        except AttributeError:
            return Response(
                {"error": "Loyalty card not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LoyaltyCardSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =====================
# ADD BONUS
# =====================

class AddBonusView(APIView):
    """
    POST:
    - Bonus qo‘shish
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BonusAmountSerializer,
        responses={200: dict},
        tags=["Loyalty"]
    )
    def post(self, request):
        serializer = BonusAmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        add_bonus(request.user, amount)

        return Response(
            {"message": "Bonus added successfully"},
            status=status.HTTP_200_OK
        )


# =====================
# SPEND BONUS
# =====================

class SpendBonusView(APIView):
    """
    POST:
    - Bonus ishlatish
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BonusAmountSerializer,
        responses={200: dict},
        tags=["Loyalty"]
    )
    def post(self, request):
        serializer = BonusAmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        spend_bonus(request.user, amount)

        return Response(
            {"message": "Bonus spent successfully"},
            status=status.HTTP_200_OK
        )


# =====================
# WALLET HISTORY
# =====================

class WalletHistoryView(APIView):
    """
    GET:
    - Wallet transaction tarixini qaytaradi
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=WalletTransactionSerializer(many=True),
        tags=["Loyalty"]
    )
    def get(self, request):
        transactions = (
            request.user.wallet_transactions
            .all()
            .order_by("-created_at")
        )

        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =====================
# CREATE ORDER
# =====================

class CreateOrderView(APIView):
    """
    POST:
    - Order yaratish
    - Bonus qo‘shish yoki ishlatish
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CreateOrderSerializer,
        responses={201: dict},
        tags=["Loyalty"]
    )
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        total_amount = serializer.validated_data["total_amount"]
        bonus_amount = serializer.validated_data["bonus_amount"]

        order = process_order(
            user=request.user,
            total_amount=total_amount,
            bonus_amount=bonus_amount
        )

        return Response(
            {
                "order_id": order.id,
                "bonus_processed": bonus_amount
            },
            status=status.HTTP_201_CREATED
        )
