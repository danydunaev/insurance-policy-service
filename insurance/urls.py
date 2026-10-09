"""Маршрутизация верхнего уровня проекта insurance."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("users/", include("web_users.urls")),
    path("policies/", include("web_policies.urls")),
]

# Обработчик ошибки 404 (собственная страница проекта)
handler404 = "homepage.views.page_not_found"