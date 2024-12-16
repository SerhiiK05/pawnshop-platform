from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.services.token_service import account_activation_token

from accounts.models import CustomUser



class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")
        self.activate_url_name = "accounts:activate"

        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "strong_password123",
            "password2": "strong_password123",
        }
        self.user = CustomUser.objects.create_user(
            username="testuser2", email="testuser2@example.com", password="testpassword"
        )

    def test_register_valid_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())
        user = CustomUser.objects.get(username="testuser")
        self.assertFalse(user.is_active)

    def test_register_invalid_user(self):
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "wrong_password"
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username="testuser").exists())

    def test_login_valid_user(self):
        response = self.client.post(
            self.login_url, {"username": "testuser2", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_user(self):
        response = self.client.post(
            self.login_url, {"username": "testuser2", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("pawnshop:index"))

    def test_activate_valid_user(self):
        user = CustomUser.objects.create_user(
            username="inactiveuser", email="inactive@example.com", password="password"
        )
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activate_url = reverse(self.activate_url_name, args=[uid, token])
        response = self.client.get(activate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you for your email confirmation.")
        user.refresh_from_db()
        self.assertTrue(user.is_active)
