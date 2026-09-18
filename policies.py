"""Работа с полисами: создание, поиск, фильтрация, сортировка.

Часть функций перенесена из ПР1 (check_policy_status,
calculate_renewal_price).
"""

from datetime import date


def check_policy_status(end_date: date) -> str:
    """Статус полиса: 'истек', 'истекает (...)' или 'активен (...)'."""
    today = date.today()
    days_left = (end_date - today).days

    if days_left < 0:
        return "истек"
    elif days_left <= 30:
        return f"истекает ({days_left} дн.)"
    else:
        return f"активен ({days_left} дн.)"


def calculate_renewal_price(
    base_price: float,
    is_accident_free: bool,
    driver_age: int,
) -> float:
    """Расчёт стоимости продления с коэффициентами."""
    price = base_price

    if is_accident_free:
        price *= 0.9

    if driver_age < 25:
        price *= 1.3

    return round(price, 2)


def _next_id(policies: list[dict]) -> int:
    """Следующий свободный ID для полиса."""
    if not policies:
        return 1
    return max(p["id"] for p in policies) + 1


def is_policy_duplicate(
    policies: list[dict],
    car_id: int,
    policy_type: str,
) -> bool:
    """Проверить, есть ли уже полис этого типа для этого авто."""
    for policy in policies:
        if (
            policy["car_id"] == car_id
            and policy["policy_type"].upper() == policy_type.upper()
        ):
            return True
    return False


def add_policy(
    policies: list[dict],
    user_id: int,
    car_id: int,
    company: str,
    policy_type: str,
    start_date: date,
    end_date: date,
    price: float,
) -> dict:
    """Добавить полис в список. Возвращает созданную запись."""
    policy = {
        "id": _next_id(policies),
        "user_id": user_id,
        "car_id": car_id,
        "company": company,
        "policy_type": policy_type.upper(),
        "start_date": start_date,
        "end_date": end_date,
        "price": float(price),
    }
    policies.append(policy)
    return policy


def find_policies_by_user(policies: list[dict], user_id: int) -> list[dict]:
    """Все полисы конкретного пользователя."""
    return [p for p in policies if p["user_id"] == user_id]


def get_expiring_soon(policies: list[dict], days: int = 30) -> list[dict]:
    """Полисы, истекающие в ближайшие N дней (и ещё не истёкшие)."""
    today = date.today()
    result = []
    for policy in policies:
        days_left = (policy["end_date"] - today).days
        if 0 <= days_left <= days:
            result.append(policy)
    return result


def sort_policies_by_price(policies: list[dict]) -> list[dict]:
    """Сортировка по цене (по возрастанию)."""
    return sorted(policies, key=lambda p: p["price"])