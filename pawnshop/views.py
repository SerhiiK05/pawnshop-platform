from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from accounts.models import CustomUser
from pawnshop.forms import (
    ItemForm,
    LoanForm,
    PaymentForm,
    ReferralBonusForm,
    ItemNameSearchForm,
)
from pawnshop.models import Item, Loan, Payment, ReferralBonus


def index(request):
    return render(request, "pawnshop/index.html")


class ItemListView(generic.ListView):
    model = Item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)

        context["search_form"] = ItemNameSearchForm()
        return context

    def get_queryset(self):
        form = ItemNameSearchForm(self.request.GET)

        if form.is_valid():
            return Item.objects.filter(name__icontains=form.cleaned_data["name"])
        return Item.objects.all()


class ItemDetailView(generic.DetailView):
    model = Item
    fields = ["name", "description", "value", "status", "user"]
    queryset = Item.objects.select_related("user")


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = Item
    form_class = ItemForm
    queryset = Item.objects.select_related("user")
    success_url = reverse_lazy("pawnshop:item-list")


class ItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Item
    fields = ["name", "description", "value", "status", "user"]
    queryset = Item.objects.select_related("user")
    success_url = reverse_lazy("pawnshop:item-list")


class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Item
    success_url = reverse_lazy("pawnshop:item-list")


class LoanListView(LoginRequiredMixin, generic.ListView):
    model = Loan
    queryset = Loan.objects.select_related("user").select_related("item")


class LoanDetailView(LoginRequiredMixin, generic.DetailView):
    model = Loan
    fields = [
        "total_amount",
        "interest_rate",
        "term",
        "status",
        "created_date",
        "item",
        "user",
    ]
    queryset = Loan.objects.select_related("user").select_related("item")


class LoanCreateView(LoginRequiredMixin, generic.CreateView):
    model = Loan
    form_class = LoanForm
    queryset = Loan.objects.select_related("user").select_related("item")
    success_url = reverse_lazy("pawnshop:loan-list")


class LoanUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Loan
    fields = [
        "total_amount",
        "interest_rate",
        "term",
        "status",
        "item",
        "user",
    ]
    queryset = Loan.objects.select_related("user").select_related("item")
    success_url = reverse_lazy("pawnshop:loan-list")


class LoanDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Loan
    success_url = reverse_lazy("pawnshop:loan-list")


class PaymentListView(LoginRequiredMixin, generic.ListView):
    model = Payment
    queryset = Payment.objects.select_related("loan")


class PaymentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Payment
    form_class = PaymentForm
    queryset = Payment.objects.select_related("loan")
    success_url = reverse_lazy("pawnshop:payment-list")

    def form_valid(self, form):
        payment = form.save(commit=False)
        loan = payment.loan

        if loan.status in ['P', 'paid_off']:
            messages.error(self.request, "This loan is already paid off.")
            return redirect("loan_detail", pk=loan.id)

        user = self.request.user
        if user.balance < payment.amount:
            messages.error(self.request, "Insufficient balance for the payment.")
            return redirect("loan_detail", pk=loan.id)

        payment.save()
        loan.total_amount -= payment.amount
        if loan.total_amount <= 0:
            loan.status = "P"
            loan.total_amount = 0
        loan.save()

        return super().form_valid(form)


class PaymentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Payment
    fields = [
        "amount",
        "payment_method",
        "payment_status",
        "loan",
        "transaction_time"
    ]
    queryset = Payment.objects.select_related("loan")
    success_url = reverse_lazy("pawnshop:payment-list")


class PaymentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Payment
    success_url = reverse_lazy("pawnshop:payment-list")


class ReferralBonusListView(LoginRequiredMixin, generic.ListView):
    model = ReferralBonus


class ReferralBonusCreateView(LoginRequiredMixin, generic.CreateView):
    model = ReferralBonus
    form_class = ReferralBonusForm
    queryset = ReferralBonus.objects.select_related("user")


class ReferralBonusUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ReferralBonus
    fields = [
        "referrer",
        "referral_code",
        "invitee",
        "invitee_email",
        "bonus_amount",
        "bonus_awarded",
        "bonus_used",
    ]
    queryset = ReferralBonus.objects.select_related("user")
    success_url = reverse_lazy("pawnshop:referral-bonus-list")


class ReferralBonusDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ReferralBonus
    success_url = reverse_lazy("pawnshop:referral-bonus-list")


class PaymentProcessView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        loan_id = request.POST.get("loan_id")
        amount = float(request.POST.get("amount", 0))
        payment_method = request.POST.get("payment_method")

        try:
            user = CustomUser.objects.get(id=user_id)
            loan = Loan.objects.get(id=loan_id)

            if user.balance < amount:
                messages.error(request, "Insufficient balance for the payment.")
                return redirect("loan_detail", pk=loan_id)

            if loan.status in ["P", "paid_off"]:
                messages.warning(request, "This loan is already paid off.")
                return redirect("loan_detail", pk=loan_id)

            with transaction.atomic():
                user.balance -= amount
                user.save()
                Payment.objects.create(
                    amount=amount,
                    payment_method=payment_method,
                    payment_status="paid",
                    loan=loan,
                )
                loan.total_amount -= amount
                if loan.total_amount <= 0:
                    loan.status = "P"
                    loan.total_amount = 0
                loan.save()
            messages.success(request, "Payment successfully processed.")
            return redirect("loan_detail", pk=loan_id)

        except Loan.DoesNotExist:
            messages.error(request, "Loan not found.")
            return redirect("loan_list")

        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("loan_list")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("loan_list")
