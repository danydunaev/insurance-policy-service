"""Маршруты приложения web_users."""

from django.urls import path
from . import views

app_name = 'web_users'

urlpatterns = [
    path('', views.users_list, name='users_list'),
]