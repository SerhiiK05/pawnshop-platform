from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase
from django.utils import timezone

from accounts.models import CustomUser
from pawnshop.models import Loan, ReferralBonus, Payment, Item


class UserModelTest(TestCase):
    def test_user_creation(self):

        user = CustomUser.objects.create(
            username="user_one",
            balance=100.50,
            role="client",
        )
        self.assertEqual(user.username, "user_one")
        self.assertEqual(user.balance, 100.50)
        self.assertEqual(user.role, "client")

    def test_user_balance_update(self):
        user = CustomUser.objects.create(
            username="user_two",
            balance=50.0,
            role="client",
        )
        user.balance += 100.0
        user.save()
        self.assertEqual(user.balance, 150.0)


class LoanModelTest(TestCase):
    def test_referral_bonus(self):
        referrer = CustomUser.objects.create_user(
            username="Anton", password="password1"
        )
        invitee = CustomUser.objects.create_user(username="Mark", password="password2")
        bonus = ReferralBonus.objects.create(
            referrer=referrer,
            invitee=invitee,
            referral_code="SomeCode",
            bonus_amount=200,
            bonus_awarded=True,
            bonus_used=False,
        )
        loan = Loan.objects.create(
            user=referrer, total_amount=500, interest_rate=12, term="9", status="A"
        )

        applied = loan.referral_bonus()
        self.assertTrue(applied)
        self.assertEqual(loan.total_amount, 700)
        bonus.refresh_from_db()
        self.assertTrue(bonus.bonus_used)

    def test_loan_status_update(self):
        loan = Loan.objects.create(
            user=CustomUser.objects.create_user(username="Anton", password="password1"),
            total_amount=1000,
            interest_rate=15,
            term="9",
            status="A",
        )
        loan.status = "C"
        loan.save()
        self.assertEqual(loan.status, "C")


class PaymentModelTest(TestCase):
    def test_payment_transaction(self):
        user = CustomUser.objects.create_user(
            username="Anton", password="password", balance=300
        )
        loan = Loan.objects.create(
            user=user, total_amount=300, interest_rate=12, term="9", status="A"
        )
        with transaction.atomic():
            payment = Payment.objects.create(
                amount=200, payment_method="cash", payment_status="paid", loan=loan,
                transaction_time = timezone.now()
            )
            loan.total_amount -= payment.amount
            loan.save()
        self.assertEqual(loan.total_amount, 100)

    def test_payment_status_update(self):
        payment = Payment.objects.create(
            amount=200,
            payment_method="card",
            payment_status="pending",
            loan=Loan.objects.create(
                user=CustomUser.objects.create_user(username="John", password="password"),
                total_amount=500,
                interest_rate=5,
                term="6",
                status="A",
            ),
            transaction_time=timezone.now()
        )
        payment.payment_status = "paid"
        payment.save()
        self.assertEqual(payment.payment_status, "paid")


class ReferralBonusModelTest(TestCase):
    def test_generate_referral_code(self):
        referrer = CustomUser.objects.create_user(
            username="referrer", password="password"
        )
        bonus = ReferralBonus.objects.create(
            referrer=referrer,
            invitee_email="test@example.com",
            bonus_amount=300,
        )
        referral_code = bonus.generate_referral_code()
        self.assertIsNotNone(referral_code)
        self.assertEqual(len(referral_code), 10)
        self.assertEqual(bonus.referral_code, referral_code)

    def test_bonus_awarded_status(self):
        referrer = CustomUser.objects.create_user(
            username="referrer", password="password"
        )
        invitee = CustomUser.objects.create_user(username="invitee", password="password")
        bonus = ReferralBonus.objects.create(
            referrer=referrer,
            invitee=invitee,
            referral_code="CODE123",
            bonus_amount=100,
            bonus_awarded=False,
            bonus_used=False,
        )
        bonus.bonus_awarded = True
        bonus.save()
        self.assertTrue(bonus.bonus_awarded)


class ItemModelTest(TestCase):
    def test_item_creation(self):
        user = CustomUser.objects.create_user(username="testuser", password="password")
        item = Item.objects.create(
            name="Laptop", description="Gaming Laptop", value=1500, status="on_pawn", user=user
        )
        self.assertEqual(item.name, "Laptop")
        self.assertEqual(item.value, 1500)
        self.assertEqual(item.status, "on_pawn")
        self.assertEqual(item.user, user)

    def test_item_value_validation(self):
        user = CustomUser.objects.create_user(username="testuser", password="password")
        item = Item(name="Phone", description="Smartphone", value=-100, status="on_pawn", user=user)
        with self.assertRaises(ValidationError) as context:
            item.clean()
            item.save()

        self.assertIn("Value should be more than 0", str(context.exception))
