"""View-функции главной страницы проекта."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """
    Собрать HTML-документ с единым каркасом.

    :param title: заголовок вкладки браузера
    :param content: содержимое страницы
    :return: HTML-строка
    """
    bootstrap_css = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{bootstrap_css}" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Сервис страховых полисов</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/users/">Пользователи</a>
                <a class="nav-link" href="/policies/">Полисы</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {content}
    </div>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Главная страница проекта."""
    content = """
    <h1 class="display-4">Сервис учёта страховых полисов</h1>
    <p class="lead">Консольное приложение, дополненное веб-интерфейсом.</p>
    <p>Основные разделы:</p>
    <a href="/users/" class="btn btn-primary me-2">Пользователи</a>
    <a href="/policies/" class="btn btn-secondary">Полисы</a>
    """
    return HttpResponse(page("Главная", content))


def page_not_found(request, exception) -> HttpResponse:
    """Обработчик ошибки 404 — собственная страница проекта."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )