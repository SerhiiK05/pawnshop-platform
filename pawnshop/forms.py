from django import forms

from pawnshop.models import Item, Loan, Payment, ReferralBonus


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "value", "status", "user"]


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["total_amount", "interest_rate", "term", "status",
                  "item", "user"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "transaction_date", "payment_method", "payment_status",
                  "loan",]


class ReferralBonusForm(forms.ModelForm):
    class Meta:
        model = ReferralBonus
        fields = ["referrer", "referral_code", "invitee", "invitee_email",]