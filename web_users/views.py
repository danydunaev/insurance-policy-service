"""View-функции для отображения пользователей."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_users

USERS_FILE = "data/users.json"


def users_list(request) -> HttpResponse:
    """Страница со списком всех пользователей."""
    users = load_users(USERS_FILE)

    if not users:
        content = """
        <h1>Пользователи</h1>
        <p class="text-muted">Список пользователей пуст.</p>
        """
        return HttpResponse(page("Пользователи", content))

    items = ""
    for user in users:
        items += (
            f'<li class="list-group-item">'
            f'<strong>{user.full_name}</strong> — '
            f'{user.phone}, {user.email}'
            f'</li>'
        )

    content = f"""
    <h1>Пользователи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Пользователи", content))