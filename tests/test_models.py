from django.db import transaction
from django.test import TestCase

from accounts.models import CustomUser
from pawnshop.models import Loan, ReferralBonus, Payment


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
                amount=200, payment_method="cash", payment_status="paid", loan=loan
            )
            loan.total_amount -= payment.amount
            loan.save()
        self.assertEqual(loan.total_amount, 100)


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
