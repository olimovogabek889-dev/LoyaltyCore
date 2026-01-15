from django.urls import path

from .views import (
    LoyaltyCardView,
    AddBonusView,
    SpendBonusView,
    WalletHistoryView,
    CreateOrderView,
)

app_name = "loyalty"

urlpatterns = [
    # =====================
    # LOYALTY CARD
    # =====================
    path(
        "card/",
        LoyaltyCardView.as_view(),
        name="loyalty-card-detail",
    ),

    # =====================
    # BONUS OPERATIONS
    # =====================
    path(
        "bonus/add/",
        AddBonusView.as_view(),
        name="bonus-add",
    ),
    path(
        "bonus/spend/",
        SpendBonusView.as_view(),
        name="bonus-spend",
    ),

    # =====================
    # WALLET
    # =====================
    path(
        "wallet/",
        WalletHistoryView.as_view(),
        name="wallet-history",
    ),

    # =====================
    # ORDERS
    # =====================
    path(
        "order/create/",
        CreateOrderView.as_view(),
        name="order-create",
    ),
]
