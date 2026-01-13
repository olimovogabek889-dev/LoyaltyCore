from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import LoyaltyCardSerializer, WalletTransactionSerializer
from .services import add_bonus, spend_bonus, process_order


class LoyaltyCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        card = request.user.loyaltycard
        return Response(LoyaltyCardSerializer(card).data)


class AddBonusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = int(request.data.get('amount'))
        add_bonus(request.user, amount)
        return Response({"status": "bonus added"})


class SpendBonusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = int(request.data.get('amount'))
        spend_bonus(request.user, amount)
        return Response({"status": "bonus spent"})


class WalletHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = request.user.wallettransaction_set.all().order_by('-created_at')
        return Response(WalletTransactionSerializer(qs, many=True).data)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        total_amount = request.data.get('total_amount')
        bonus_amount = request.data.get('bonus_amount')

        order = process_order(
            user=request.user,
            total_amount=total_amount,
            bonus_amount=bonus_amount
        )

        return Response({
            "order_id": order.id,
            "bonus_added": bonus_amount
        })
