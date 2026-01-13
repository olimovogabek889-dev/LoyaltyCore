from django.urls import path
from .views import (
    LoyaltyCardView,
    AddBonusView,
    SpendBonusView,
    WalletHistoryView,
    CreateOrderView,
)

urlpatterns = [
    path('card/', LoyaltyCardView.as_view()),
    path('bonus/add/', AddBonusView.as_view()),
    path('bonus/spend/', SpendBonusView.as_view()),
    path('wallet/', WalletHistoryView.as_view()),
    path('order/create/', CreateOrderView.as_view()),
]
