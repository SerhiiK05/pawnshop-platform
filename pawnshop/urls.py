from django.urls import path

from pawnshop.views import index

app_name = "pawnshop"

urlpatterns = [
    path("", index, name="index"),
]