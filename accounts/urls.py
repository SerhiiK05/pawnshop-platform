from django.urls import path

from accounts.views import register, login_view, logout_view, activate

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("activate/<str:uid>/<str:token>/", activate, name="activate"),
]