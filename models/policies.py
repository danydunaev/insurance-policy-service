"""Класс Policy и функции работы с полисами."""

from datetime import date

from models.cars import Car
from models.users import User


class Policy:
    """Страховой полис."""

    def __init__(
        self,
        policy_id: int,
        user: User,
        car: Car,
        company: str,
        policy_type: str,
        start_date: date,
        end_date: date,
        price: float,
    ) -> None:
        """Создать объект полиса."""
        self.id = policy_id
        self.user = user
        self.car = car
        self.company = company
        self.policy_type = policy_type.upper()
        self.start_date = start_date
        self.end_date = end_date
        self.price = float(price)

    def __str__(self) -> str:
        """Строковое представление полиса."""
        return (
            f"[{self.id}] {self.policy_type} — {self.car.license_plate} "
            f"({self.user.full_name}), {self.company}, {self.price:.2f} руб."
        )

    def check_status(self) -> str:
        """Проверить срок действия полиса."""
        today = date.today()
        days_left = (self.end_date - today).days

        if days_left < 0:
            return "истек"
        elif days_left <= 30:
            return f"истекает ({days_left} дн.)"
        else:
            return f"активен ({days_left} дн.)"

    def calculate_renewal_price(
        self,
        is_accident_free: bool,
        driver_age: int,
    ) -> float:
        """Рассчитать стоимость продления полиса."""
        new_price = self.price

        if is_accident_free:
            new_price *= 0.9

        if driver_age < 25:
            new_price *= 1.3

        return round(new_price, 2)

    @classmethod
    def from_data(
        cls,
        data: dict,
        users: list[User],
        cars: list[Car],
    ) -> "Policy | None":
        """Создать Policy из словаря, найдя объекты User и Car."""
        user = next((u for u in users if u.id == data["user_id"]), None)
        car = next((c for c in cars if c.id == data["car_id"]), None)
        if user is None or car is None:
            return None

        return cls(
            policy_id=data["id"],
            user=user,
            car=car,
            company=data["company"],
            policy_type=data["policy_type"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            price=data["price"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "car_id": self.car.id,
            "company": self.company,
            "policy_type": self.policy_type,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "price": self.price,
        }


def _next_id(policies: list[Policy]) -> int:
    """Следующий свободный ID."""
    if not policies:
        return 1
    return max(p.id for p in policies) + 1


def add_policy(
    policies: list[Policy],
    user: User,
    car: Car,
    company: str,
    policy_type: str,
    start_date: date,
    end_date: date,
    price: float,
) -> Policy:
    """Создать объект Policy и добавить его в коллекцию."""
    policy = Policy(
        _next_id(policies),
        user,
        car,
        company,
        policy_type,
        start_date,
        end_date,
        price,
    )
    policies.append(policy)
    return policy


def is_policy_duplicate(
    policies: list[Policy],
    car: Car,
    policy_type: str,
) -> bool:
    """Проверить, есть ли уже полис такого типа для этого авто."""
    return any(
        p.car.id == car.id and p.policy_type == policy_type.upper()
        for p in policies
    )


def find_policies_by_user(
    policies: list[Policy],
    user: User,
) -> list[Policy]:
    """Все полисы конкретного пользователя."""
    return [p for p in policies if p.user.id == user.id]


def get_expiring_soon(
    policies: list[Policy],
    days: int = 30,
) -> list[Policy]:
    """Полисы, истекающие в ближайшие N дней (и ещё не истёкшие)."""
    today = date.today()
    result = []
    for policy in policies:
        days_left = (policy.end_date - today).days
        if 0 <= days_left <= days:
            result.append(policy)
    return result


def sort_policies_by_price(policies: list[Policy]) -> list[Policy]:
    """Сортировка по цене (по возрастанию)."""
    return sorted(policies, key=lambda p: p.price)