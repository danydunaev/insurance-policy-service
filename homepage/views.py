"""
View-функции приложения homepage.
ПР6: HTML вынесен в шаблоны, функция page() больше не используется.
"""

from django.shortcuts import render

# ============================================================
# ВОПРОС ТАБЛИЦЫ №9: Обработка HTTP-запроса
# Путь GET /:
#   1. ROOT_URLCONF (insurance/urls.py) видит '' → include('homepage.urls')
#   2. homepage/urls.py сопоставляет '' с views.index
#   3. index(request) вызывается
#   4. index() возвращает render(request, 'homepage/index.html')
#   5. render() формирует HttpResponse с HTML
#   6. Django отдаёт HttpResponse браузеру
#
# ВОПРОС ТАБЛИЦЫ №10: Взаимодействие запроса и представления
# request — HttpRequest, создаётся Django, передаётся первым аргументом.
# Возвращать нужно HttpResponse (или его подкласс).
# Если вернуть str, будет AttributeError: 'str' object has no attribute 'get'.
# ============================================================


def index(request):
    """
    Главная страница.

    ВОПРОС ТАБЛИЦЫ №11: Формирование HTML-страницы
    Было (ПР5): content = "..." → page() → HttpResponse
    Стало (ПР6): render() → homepage/index.html → base.html
    HTML формируется шаблоном, а не Python-кодом.
    """
    return render(request, 'homepage/index.html')


def page_not_found(request, exception):
    """Собственная страница 404."""
    return render(request, 'homepage/404.html', status=404)