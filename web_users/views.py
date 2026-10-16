"""
View-функции приложения web_users.
ПР6: HTML вынесен в шаблон users_list.html.
"""

from django.shortcuts import render
from storage import load_users

USERS_FILE = "data/users.json"


def users_list(request):
    """
    Страница со списком всех пользователей.

    ВОПРОС ТАБЛИЦЫ №27 (оценивание): Бизнес-логика
    Загрузка данных — во view, а не в шаблоне.
    Шаблон только отображает данные через {{ }} и {% for %}.
    """
    users = load_users(USERS_FILE)
    context = {'users': users}
    return render(request, 'web_users/users_list.html', context)