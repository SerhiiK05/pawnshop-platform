from django.urls import reverse_lazy
from django.views import generic

from pawnshop.models import Item, Loan, Payment, ReferralBonus, User


# Create your views here.
def index():
    pass


class UserListView(generic.ListView):
    model = User



class UserDetailView(generic.DetailView):
    model = User
    fields = ["username", "email", "first_name",
              "last_name", "balance", "role", "created_at",
              "updated_at",]


class UserCreateView(generic.CreateView):
    model = User
    fields = ["username", "email", "first_name",
              "last_name", "balance", "role", "created_at",
              "updated_at",]
    success_url = reverse_lazy("pawnshop:user-list")


class UserUpdateView(generic.UpdateView):
    model = User
    fields = ["username", "email", "first_name",
              "last_name", "balance", "role", "created_at",
              "updated_at",]
    success_url = reverse_lazy("pawnshop:user-list")


class UserDeleteView(generic.DeleteView):
    model = User
    success_url = reverse_lazy("pawnshop:user-list")


class ItemListView(generic.ListView):
    model = Item


class ItemDetailView(generic.DetailView):
    model = Item
    fields = ["name", "description", "value", "status", "user"]
    queryset = Item.objects.select_related("user")


class ItemCreateView(generic.CreateView):
    model = Item
    fields = ["name", "description", "value", "status", "user"]
    queryset = Item.objects.select_related("user")
    success_url = reverse_lazy("pawnshop:item-list")


class ItemUpdateView(generic.UpdateView):
    model = Item
    fields = ["name", "description", "value", "status", "user"]
    queryset = Item.objects.select_related("user")
    success_url = reverse_lazy("pawnshop:item-list")


class ItemDeleteView(generic.DeleteView):
    model = Item
    success_url = reverse_lazy("pawnshop:item-list")


class LoanListView(generic.ListView):
    model = Loan


class LoanDetailView(generic.DetailView):
    model = Loan
    fields = ["total_amount", "interest_rate", "term", "status", "created_date",
              "item", "user"]
    queryset = Loan.objects.select_related("user").select_related("item")


class LoanCreateView(generic.CreateView):
    model = Loan
    fields = ["total_amount", "interest_rate", "term", "status", "created_date",
              "item", "user"]
    queryset = Loan.objects.select_related("user").select_related("item")
    success_url = reverse_lazy("pawnshop:loan-list")


class LoanUpdateView(generic.UpdateView):
    model = Loan
    fields = ["total_amount", "interest_rate", "term", "status", "created_date",
              "item", "user"]
    queryset = Loan.objects.select_related("user").select_related("item")
    success_url = reverse_lazy("pawnshop:loan-list")


class LoanDeleteView(generic.DeleteView):
    model = Loan
    success_url = reverse_lazy("pawnshop:loan-list")


class PaymentListView(generic.ListView):
    model = Payment


class PaymentDetailView(generic.DetailView):
    model = Payment
    fields = ["amount", "transaction_date", "payment_method", "payment_status",
              "loan", ]
    queryset = Payment.objects.select_related("loan")


class PaymentCreateView(generic.CreateView):
    model = Payment
    fields = ["amount", "transaction_date", "payment_method", "payment_status",
              "loan", ]
    queryset = Payment.objects.select_related("loan")
    success_url = reverse_lazy("pawnshop:payment-list")


class PaymentUpdateView(generic.UpdateView):
    model = Payment
    fields = ["amount", "transaction_date", "payment_method", "payment_status",
              "loan", ]
    queryset = Payment.objects.select_related("loan")
    success_url = reverse_lazy("pawnshop:payment-list")


class PaymentDeleteView(generic.DeleteView):
    model = Payment
    success_url = reverse_lazy("pawnshop:payment-list")


class ReferralBonusListView(generic.ListView):
    model = ReferralBonus


class ReferralBonusCreateView(generic.CreateView):
    model = ReferralBonus
    fields = ["referrer", "referral_code", "invitee", "invitee_email",
              "bonus_amount", "bonus_awarded", "bonus_used",]
    queryset = ReferralBonus.objects.select_related("user")


class ReferralBonusUpdateView(generic.UpdateView):
    model = ReferralBonus
    fields = ["referrer", "referral_code", "invitee", "invitee_email",
              "bonus_amount", "bonus_awarded", "bonus_used",]
    queryset = ReferralBonus.objects.select_related("user")
    success_url = reverse_lazy("pawnshop:referral-bonus-list")


class ReferralBonusDeleteView(generic.DeleteView):
    model = ReferralBonus
    success_url = reverse_lazy("pawnshop:referral-bonus-list")