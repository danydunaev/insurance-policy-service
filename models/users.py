"""Класс User и функции работы с пользователями."""


class User:
    """Пользователь (владелец автомобиля)."""

    def __init__(
        self,
        user_id: int,
        full_name: str,
        phone: str,
        email: str,
    ) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.full_name = full_name
        self.phone = phone
        self.email = email

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"[{self.id}] {self.full_name}, {self.phone}"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать объект User из словаря (JSON)."""
        return cls(
            user_id=data["id"],
            full_name=data["full_name"],
            phone=data["phone"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email,
        }


def _next_id(users: list[User]) -> int:
    """Следующий свободный ID."""
    if not users:
        return 1
    return max(u.id for u in users) + 1


def add_user(
    users: list[User],
    full_name: str,
    phone: str,
    email: str,
) -> User:
    """Создать объект User и добавить его в коллекцию."""
    user = User(_next_id(users), full_name, phone, email)
    users.append(user)
    return user


def get_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по ID."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user_by_name(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке в ФИО."""
    query_lower = query.lower()
    return [u for u in users if query_lower in u.full_name.lower()]