"""
View-функции приложения web_policies.
ПР6: HTML вынесен в шаблоны policy_list.html и policy_detail.html.
"""

from django.shortcuts import render
from storage import load_cars, load_policies, load_users

USERS_FILE = "data/users.json"
CARS_FILE = "data/cars.json"
POLICIES_FILE = "data/policies.json"

# ============================================================
# ВОПРОС ТАБЛИЦЫ №8: Работа конвертера URL
# /policies/abc/ — не совпадёт с <int:policy_id>, Django вернёт 404
#                  ещё на этапе маршрутизации; view не вызовется.
# /policies/999/ — совпадёт, policy_id=999 передастся в view.
# ============================================================


def policies_list(request):
    """Страница со списком всех полисов."""
    users = load_users(USERS_FILE)
    cars = load_cars(CARS_FILE, users)
    policies = load_policies(POLICIES_FILE, users, cars)
    context = {'policies': policies}
    return render(request, 'web_policies/policy_list.html', context)


def policy_detail(request, policy_id):
    """
    Страница конкретного полиса.

    ВОПРОС ТАБЛИЦЫ №16 (оценивание): Обработка отсутствия
    find возвращает None, если полис не найден.
    status=404 if policy is None else 200 — HTTP-статус 404.
    """
    users = load_users(USERS_FILE)
    cars = load_cars(CARS_FILE, users)
    policies = load_policies(POLICIES_FILE, users, cars)

    policy = next((p for p in policies if p.id == policy_id), None)

    context = {'policy': policy}
    return render(
        request,
        'web_policies/policy_detail.html',
        context,
        status=404 if policy is None else 200,
    )