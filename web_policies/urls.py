"""Маршруты приложения web_policies."""

from django.urls import path
from . import views

# ============================================================
# ВОПРОС ТАБЛИЦЫ №7: Связь маршрута и view-функции
# path('<int:policy_id>/', views.policy_detail, name='policy_detail')
#   - <int:policy_id> — конвертер, захватывает число;
#   - views.policy_detail — view-функция;
#   - name='policy_detail' — имя для {% url %}.
# Если переименовать функцию, достаточно поменять views.policy_detail →
# views.show_policy. URL и шаблоны не изменятся, т.к. ссылки строятся
# по name=.
# ============================================================

app_name = 'web_policies'

urlpatterns = [
    path('', views.policies_list, name='policies_list'),
    path('<int:policy_id>/', views.policy_detail, name='policy_detail'),
]