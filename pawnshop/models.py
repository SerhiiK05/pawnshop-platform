import string
from random import random

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_CHOICES = [
        ("user", "User"),
        ("client", "Client"),
    ]
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    role = models.CharField(choices=USER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    ITEM_STATUS_CHOICES = [
        ("on_pawn", "On Pawn"),
        ("redeemed", "Redeemed"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=ITEM_STATUS_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="items"
    )


class Loan(models.Model):
    LOAN_TERM_CHOICES = [
        ("3", "3 months"),
        ("6", "6 months"),
        ("9", "9 months"),
        ("12", "12 months"),
    ]

    LOAN_STATUS_CHOICES = [
        ("W", "waiting for approve"),
        ("A", "approved"),
        ("R", "rejected"),
        ("P", "paid off"),
    ]
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.IntegerField(choices=LOAN_TERM_CHOICES)
    status = models.CharField(choices=LOAN_STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    item = models.OneToOneField(
        Item,
        on_delete=models.SET_NULL,
        related_name="loan_item"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="loans_user"
    )

    def referral_bonus(self):
        referral_bonus = ReferralBonus.objects.filter(referrer=self.user)
        for bonus in referral_bonus:
            if bonus.bonus_awarded and (bonus.bonus_used is False):
                self.total_amount += bonus.bonus_amount
                self.save()
                return True
        return False


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES)
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="payments"
    )


class ReferralBonus(models.Model):
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="referrer"
    )
    referral_code = models.CharField(max_length=100, unique=True)
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        unique=True,
        on_delete=models.SET_NULL,
        related_name="invitee"
    )
    invitee_email = models.EmailField(unique=True)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_awarded = models.BooleanField(default=False)
    bonus_used = models.BooleanField(default=False)

    def generate_referral_code(self):
        if not self.referral_code:
            code = "".join(random.choices(string.ascii_uppercase, k=10))
            self.referral_code = code
            self.save()
        return self.referral_code

    def assign_random_bonus(self):
        if self.bonus_awarded:
            possible_bonuses = [100, 200, 300, 400, 500]
            self.bonus_amount = random.choice(possible_bonuses)

    def referral_bonus_usage(self):
        if Loan.referral_bonus():
            self.bonus_amount = 0
            self.bonus_used = True
            self.save()
            return True
        return False