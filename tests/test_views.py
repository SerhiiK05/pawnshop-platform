from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from pawnshop.models import Loan, Item, Payment, ReferralBonus


class LoanListViewTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username="Anton", balance=500)
        Loan.objects.create(
            user=user, total_amount=100, interest_rate=10, term="3", status="A"
        )

    def test_loan_list_view(self):
        self.client.login(username='Anton', password='password123')

        url = reverse("pawnshop:loan-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PaymentCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="Anton", password="password123"
        )
        self.item = Item.objects.create(
            name="Knife",
            description="Old one",
            value=600,
            status="on_pawn",
            user=self.user,
        )
        self.loan = Loan.objects.create(
            total_amount=600,
            interest_rate=5,
            term="12",
            status="A",
            item=self.item,
            user=self.user,
        )
        self.url = reverse("pawnshop:payment-create")


    def test_payment_create_view_post(self):
        data = {
            "amount": 90,
            "payment_method": "card",
            "payment_status": "paid",
            "loan": self.loan.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Payment.objects.filter(amount=90).exists())

    def test_payment_not_created_with_invalid_data(self):
        data = {
            "amount": "invalid",
            "payment_method": "",  # Missing required field
            "payment_status": "pending",
            "loan": self.loan.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Payment.objects.count(), 0)

    def test_payment_creation_updates_loan_status(self):
        data = {
            "amount": 600,
            "payment_method": "card",
            "payment_status": "paid",
            "loan": self.loan.id,
        }
        self.client.post(self.url, data)
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, "A")


class LoanModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="Anton", password="password123")
        self.item = Item.objects.create(
            name="Ring", description="Gold ring", value=1500, status="on_pawn", user=self.user
        )

    def test_loan_creation(self):
        loan = Loan.objects.create(
            user=self.user, total_amount=2000, interest_rate=15, term="12", status="A", item=self.item
        )
        self.assertEqual(loan.total_amount, 2000)
        self.assertEqual(loan.status, "A")
        self.assertEqual(loan.item.name, "Ring")


class ItemModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="Anton", password="password123")

    def test_item_creation(self):
        item = Item.objects.create(
            name="Gold Necklace", description="Luxury item", value=3000, status="on_pawn", user=self.user
        )
        self.assertEqual(item.name, "Gold Necklace")
        self.assertEqual(item.value, 3000)
        self.assertEqual(item.status, "on_pawn")

    def test_item_status_update(self):
        item = Item.objects.create(
            name="Silver Bracelet", description="Handcrafted", value=2000, status="available", user=self.user
        )
        item.status = "sold"
        item.save()
        self.assertEqual(item.status, "sold")


class ReferralBonusModelTest(TestCase):
    def setUp(self):
        self.referrer = CustomUser.objects.create_user(username="Referrer", password="password1")
        self.invitee = CustomUser.objects.create_user(username="Invitee", password="password2")

    def test_referral_bonus_creation(self):
        referral_bonus = ReferralBonus.objects.create(
            referrer=self.referrer,
            invitee=self.invitee,
            referral_code="CODE123",
            bonus_amount=100,
            bonus_awarded=False,
            bonus_used=False,
        )
        self.assertEqual(referral_bonus.referral_code, "CODE123")
        self.assertEqual(referral_bonus.bonus_amount, 100)
        self.assertFalse(referral_bonus.bonus_awarded)
        self.assertFalse(referral_bonus.bonus_used)

    def test_referral_bonus_awarded(self):
        referral_bonus = ReferralBonus.objects.create(
            referrer=self.referrer,
            invitee=self.invitee,
            referral_code="CODE123",
            bonus_amount=100,
            bonus_awarded=True,
            bonus_used=False,
        )
        self.assertTrue(referral_bonus.bonus_awarded)
        referral_bonus.bonus_used = True
        referral_bonus.save()
        self.assertTrue(referral_bonus.bonus_used)

    def test_referral_bonus_code_uniqueness(self):
        ReferralBonus.objects.create(
            referrer=self.referrer,
            invitee=self.invitee,
            referral_code="UNIQUECODE",
            bonus_amount=150,
        )
        with self.assertRaises(Exception):
            ReferralBonus.objects.create(
                referrer=self.referrer,
                invitee=self.invitee,
                referral_code="UNIQUECODE",
                bonus_amount=200,
            )
