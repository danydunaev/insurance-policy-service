"""Тесты для модуля users."""

from users import add_user, find_user_by_name, get_user_by_id


def test_add_user():
    """add_user добавляет запись с ID."""
    users: dict[int, dict] = {}
    user = add_user(users, "Иванов Иван", "+7-999-000-00-00", "i@test.ru")
    assert len(users) == 1
    assert user["id"] == 1
    assert user["full_name"] == "Иванов Иван"


def test_get_user_by_id():
    """get_user_by_id возвращает запись или None."""
    users: dict[int, dict] = {}
    add_user(users, "Петров Пётр", "+7-999-111-11-11", "p@test.ru")
    assert get_user_by_id(users, 1) is not None
    assert get_user_by_id(users, 99) is None


def test_find_user_by_name():
    """Поиск по подстроке в ФИО."""
    users: dict[int, dict] = {}
    add_user(users, "Иванов Иван", "+7", "a@test.ru")
    add_user(users, "Петров Пётр", "+7", "b@test.ru")
    result = find_user_by_name(users, "иван")
    assert len(result) == 1
    assert result[0]["full_name"] == "Иванов Иван"


def test_find_user_empty_result():
    """Пустой результат, если совпадений нет."""
    users: dict[int, dict] = {}
    add_user(users, "Иванов Иван", "+7", "a@test.ru")
    assert find_user_by_name(users, "Сидоров") == []