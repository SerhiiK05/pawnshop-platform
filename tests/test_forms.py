from django.test import TestCase
from accounts.models import CustomUser
from pawnshop.models import Item, Loan, ReferralBonus
from pawnshop.forms import ItemForm, LoanForm, PaymentForm, ReferralBonusForm

class ItemFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )

    def test_form_is_valid(self):
        form_data = {
            "name": "Laptop",
            "description": "Gaming laptop",
            "value": 3000,
            "status": "on_pawn",
            "user": self.user,
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_value_validation(self):
        form_data = {
            "name": "Old Phone",
            "description": "Old phone very",
            "value": -100,
            "status": "on_pawn",
            "user": self.user,
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["value"], ["Value should be more than 0"])


class LoanFormTest(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1", password="password123"
        )
        self.user2 = CustomUser.objects.create_user(
            username="testuser2", password="password123"
        )
        self.item = Item.objects.create(
            name="Ring",
            value=400,
            status="on_pawn",
            user=self.user1,
        )

    def test_form_is_valid(self):
        form_data = {
            "total_amount": 4000,
            "interest_rate": 15,
            "term": "9",
            "status": "W",
            "item": self.item,
            "user": self.user2,
        }
        form = LoanForm(data=form_data)
        self.assertTrue(form.is_valid())


class PaymentFormTest(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1", password="password123"
        )
        self.user2 = CustomUser.objects.create_user(
            username="testuser2", password="password123"
        )
        self.item = Item.objects.create(
            name="Gold Ring",
            value=14400,
            status="on_pawn",
            user=self.user1,
        )
        self.loan = Loan.objects.create(
            total_amount=1000,
            interest_rate=5,
            term="3",
            status="W",
            item=self.item,
            user=self.user2,
        )

    def test_form_is_valid(self):
        form_data = {
            "amount": 500,
            "payment_method": "cash",
            "payment_status": "paid",
            "loan": self.loan,
        }
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_amount_validation(self):
        form_data = {
            "amount": -50,
            "payment_method": "card",
            "payment_status": "paid",
            "loan": self.loan,
        }
        form = PaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["amount"], ["Amount should be more than 0"])


class ReferralBonusFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="Anton", password="password123"
        )

    def test_form_is_valid(self):
        form_data = {
            "referrer": self.user,
            "referral_code": "ABCCCADDDD",
            "invitee": self.user,
            "invitee_email": "Arcer1@example.com",
        }
        form = ReferralBonusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_referral_code_unique(self):
        ReferralBonus.objects.create(
            referrer=self.user,
            referral_code="ABCCCADDDD",
            invitee=self.user,
            invitee_email="adcer1@example.com",
        )
        form_data = {
            "referrer": self.user,
            "referral_code": "ABCCCADDDD",
            "invitee": self.user,
            "invitee_email": "MishaM2@example.com",
        }
        form = ReferralBonusForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["referral_code"],
            ["Referral-bonus with this Referral code already exists."],
        )
