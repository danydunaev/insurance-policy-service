"""Тесты для моделей пользователей."""

from models.users import User, add_user, find_user_by_name, get_user_by_id


def test_user_creation():
    """Объект User создаётся с корректными атрибутами."""
    user = User(1, "Иванов Иван", "+7-999-000-00-00", "i@test.ru")
    assert user.id == 1
    assert user.full_name == "Иванов Иван"
    assert user.phone == "+7-999-000-00-00"
    assert user.email == "i@test.ru"


def test_user_str():
    """Строковое представление User содержит данные."""
    user = User(1, "Иванов Иван", "+7-999-000-00-00", "i@test.ru")
    text = str(user)
    assert "Иванов Иван" in text
    assert "[1]" in text


def test_user_from_data():
    """from_data создаёт объект User из словаря."""
    data = {
        "id": 5,
        "full_name": "Петров Пётр",
        "phone": "+7-999-111-11-11",
        "email": "p@test.ru",
    }
    user = User.from_data(data)
    assert user.id == 5
    assert user.full_name == "Петров Пётр"


def test_add_user():
    """add_user создаёт объект и добавляет его в коллекцию."""
    users: list[User] = []
    user = add_user(users, "Иванов Иван", "+7", "a@test.ru")
    assert len(users) == 1
    assert user.id == 1
    assert users[0] is user


def test_get_user_by_id():
    """Поиск по ID возвращает объект или None."""
    users: list[User] = []
    add_user(users, "Иванов Иван", "+7", "a@test.ru")
    assert get_user_by_id(users, 1) is not None
    assert get_user_by_id(users, 99) is None


def test_find_user_by_name():
    """Поиск по подстроке в ФИО."""
    users: list[User] = []
    add_user(users, "Иванов Иван", "+7", "a@test.ru")
    add_user(users, "Петров Пётр", "+7", "b@test.ru")
    result = find_user_by_name(users, "иван")
    assert len(result) == 1
    assert result[0].full_name == "Иванов Иван"