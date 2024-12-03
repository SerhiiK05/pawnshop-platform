from django.urls import path

from pawnshop.views import (
    index,
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    LoanListView,
    LoanDetailView,
    LoanCreateView,
    LoanUpdateView,
    LoanDeleteView,
    PaymentListView,
    PaymentCreateView,
    PaymentUpdateView,
    PaymentDeleteView,
    ReferralBonusListView,
    ReferralBonusCreateView,
    ReferralBonusUpdateView,
    ReferralBonusDeleteView,
    PaymentProcessView,
)

app_name = "pawnshop"


urlpatterns = [
    path("", index, name="index"),
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("items/create", ItemCreateView.as_view(), name="item-create"),
    path("items/<int:pk>/update/", ItemUpdateView.as_view(), name="item-update"),
    path("items/<int:pk>/delete", ItemDeleteView.as_view(), name="item-delete"),
    path("loans/", LoanListView.as_view(), name="loan-list"),
    path("loans/<int:pk>/", LoanDetailView.as_view(), name="loan-detail"),
    path("loans/create", LoanCreateView.as_view(), name="loan-create"),
    path("loans/<int:pk>/update/", LoanUpdateView.as_view(), name="loan-update"),
    path("loans/<int:pk>/delete", LoanDeleteView.as_view(), name="loan-delete"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/create", PaymentCreateView.as_view(), name="payment-create"),
    path(
        "payments/<int:pk>/update/", PaymentUpdateView.as_view(), name="payment-update"
    ),
    path(
        "payments/<int:pk>/delete", PaymentDeleteView.as_view(), name="payment-delete"
    ),
    path(
        "referral_bonuses/", ReferralBonusListView.as_view(), name="referral-bonus-list"
    ),
    path(
        "referral_bonuses/create",
        ReferralBonusCreateView.as_view(),
        name="referral-bonus-create",
    ),
    path(
        "referral_bonuses/<int:pk>/update/",
        ReferralBonusUpdateView.as_view(),
        name="referral-bonus-update",
    ),
    path(
        "referral_bonuses/<int:pk>/delete",
        ReferralBonusDeleteView.as_view(),
        name="referral-bonus-delete",
    ),
    path("payment_process/", PaymentProcessView.as_view(), name="payment-process"),
]
