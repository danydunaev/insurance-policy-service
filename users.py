"""Работа с пользователями (владельцами автомобилей)."""


def _next_id(users: dict[int, dict]) -> int:
    """Вернуть следующий свободный ID."""
    if not users:
        return 1
    return max(users.keys()) + 1


def add_user(
    users: dict[int, dict],
    full_name: str,
    phone: str,
    email: str,
) -> dict:
    """Добавить пользователя в словарь. Возвращает созданную запись."""
    user_id = _next_id(users)
    user = {
        "id": user_id,
        "full_name": full_name,
        "phone": phone,
        "email": email,
    }
    users[user_id] = user
    return user


def get_user_by_id(users: dict[int, dict], user_id: int) -> dict | None:
    """Найти пользователя по ID."""
    return users.get(user_id)


def find_user_by_name(users: dict[int, dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке в ФИО."""
    query_lower = query.lower()
    return [
        user
        for user in users.values()
        if query_lower in user["full_name"].lower()
    ]