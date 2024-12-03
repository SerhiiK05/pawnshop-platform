from django.test import TestCase

from accounts.models import CustomUser
from pawnshop.models import Item, Loan, ReferralBonus
from pawnshop.forms import ItemForm, LoanForm, PaymentForm, ReferralBonusForm


class ItemFormTest(TestCase):

    def test_form_is_valid(self):
        form_data = {
            "name": "Laptop",
            "description": "Gaming laptop",
            "value": 3000,
            "status": "on_pawn",
            "user": CustomUser.objects.create_user(
                username="testa", password="password123"
            ),
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_value_validation(self):
        form_data = {
            "name": "Old Phone",
            "description": "Old phone very",
            "value": -100,
            "status": "on_pawn",
            "user": CustomUser.objects.create_user(
                username="testtt", password="password12"
            ),
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["value"], ["Value should be more than 0"])


class LoanFormTest(TestCase):

    def test_form_is_valid(self):
        form_data = {
            "total_amount": 4000,
            "interest_rate": 15,
            "term": "9",
            "status": "W",
            "item": Item.objects.create(
                name="Ring",
                value=400,
                status="on_pawn",
                user=CustomUser.objects.create_user(
                    username="test1", password="password3"
                ),
            ),
            "user": CustomUser.objects.create_user(
                username="test2", password="password23"
            ),
        }
        form = LoanForm(data=form_data)
        self.assertTrue(form.is_valid())


class PaymentFormTest(TestCase):

    def test_form_is_valid(self):
        loan = Loan.objects.create(
            total_amount=1000,
            interest_rate=5,
            term="3",
            status="W",
            item=Item.objects.create(
                name="Gold Ring",
                value=14400,
                status="on_pawn",
                user=CustomUser.objects.create_user(
                    username="test1", password="password123"
                ),
            ),
            user=CustomUser.objects.create_user(
                username="test2", password="password123"
            ),
        )
        form_data = {
            "amount": 500,
            "payment_method": "cash",
            "payment_status": "paid",
            "loan": loan,
        }
        form = PaymentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_amount_validation(self):
        loan = Loan.objects.create(
            total_amount=1000,
            interest_rate=5,
            term="3",
            status="W",
            item=Item.objects.create(
                name="Ring",
                value=500,
                status="on_pawn",
                user=CustomUser.objects.create_user(
                    username="rrrrr", password="password1"
                ),
            ),
            user=CustomUser.objects.create_user(username="rrr", password="password1"),
        )
        form_data = {
            "amount": -50,
            "payment_method": "card",
            "payment_status": "paid",
            "loan": loan,
        }
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["amount"], ["Amount should be more than 0"])


class ReferralBonusFormTest(TestCase):

    def test_form_is_valid(self):
        user = CustomUser.objects.create_user(username="Anton", password="password1")
        form_data = {
            "referrer": user,
            "referral_code": "ABCCCADDDD",
            "invitee": user,
            "invitee_email": "Arcer1@example.com",
        }
        form = ReferralBonusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_referral_code_unique(self):
        user = CustomUser.objects.create_user(username="Anton", password="password12")
        ReferralBonus.objects.create(
            referrer=user,
            referral_code="ABCCCADDDD",
            invitee=user,
            invitee_email="adcer1@example.com",
        )
        form_data = {
            "referrer": user,
            "referral_code": "ABCCCADDDD",
            "invitee": user,
            "invitee_email": "MishaM2@example.com",
        }
        form = ReferralBonusForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["referral_code"],
            ["Referral-bonus with this " "Referral code already exists."],
        )
