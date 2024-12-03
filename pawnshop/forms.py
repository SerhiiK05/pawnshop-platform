from django import forms
from django.core.exceptions import ValidationError

from pawnshop.models import Item, Loan, Payment, ReferralBonus


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "value", "status", "user"]

    def clean_value(self):
        value = self.cleaned_data["value"]
        if value < 0:
            raise ValidationError("Value should be more than 0")
        return value


class ItemNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["total_amount", "interest_rate", "term", "status", "item", "user"]

        def clean_interest_rate(self):
            interest_rate = self.cleaned_date["interest_rate"]
            if interest_rate > 100:
                raise ValidationError("Interest rate should not be more than 100")
            return interest_rate


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "payment_method", "payment_status", "loan"]

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount < 0:
            raise ValidationError("Amount should be more than 0")
        return amount


class ReferralBonusForm(forms.ModelForm):
    class Meta:
        model = ReferralBonus
        fields = [
            "referrer",
            "referral_code",
            "invitee",
            "invitee_email",
        ]
