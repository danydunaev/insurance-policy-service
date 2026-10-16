"""
Корневой URLconf проекта «Сервис учёта страховых полисов».
"""

# ============================================================
# ВОПРОС ТАБЛИЦЫ №1: Корневой urls.py
# Точка входа маршрутизации. Подключает URLconf приложений
# через include() и связывает префиксы с приложениями.
#
# ВОПРОС ТАБЛИЦЫ №6: Маршрутизация между URLconf
# URL /policies/999/:
#   1. Корневой urls.py видит 'policies/' → include('web_policies.urls')
#   2. web_policies/urls.py видит '<int:policy_id>/' → policy_detail(999)
#   3. include() нужен для разделения маршрутов по приложениям —
#      приложение становится переносимым.
# ============================================================

from django.contrib import admin
from django.urls import path, include
from homepage.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('users/', include('web_users.urls')),
    path('policies/', include('web_policies.urls')),
]

handler404 = page_not_found