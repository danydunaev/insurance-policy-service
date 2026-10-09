"""Маршруты приложения web_policies."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.policies_list, name="policies_list"),
    path("<int:policy_id>/", views.policy_detail, name="policy_detail"),
]