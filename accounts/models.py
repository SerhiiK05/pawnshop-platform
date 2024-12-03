from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_CHOICES = [
        ("user", "User"),
        ("client", "Client"),
    ]
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    role = models.CharField(max_length=10, choices=USER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
