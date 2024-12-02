from django.test import TestCase
from django.urls import reverse
from pawnshop.models import Loan, User, Item, Payment


class LoanListViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="Anton", balance=500)
        Loan.objects.create(
            user=user,
            total_amount=100,
            interest_rate=10,
            term="3",
            status="A"
        )

    def test_loan_list_view(self):
        url = reverse("pawnshop:loan-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PaymentCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Anton", password="password123")
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

    def test_payment_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pawnshop/payment_form.html")

    def test_payment_create_view_post(self):
        data = {
            "amount": 90,
            "payment_method": "card",
            "payment_status": "paid",
            "loan": self.loan.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Payment.objects.filter(amount=90).exists())