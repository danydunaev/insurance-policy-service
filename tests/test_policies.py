"""Тесты для моделей полисов."""

from datetime import date, timedelta

from models.cars import Car
from models.policies import (
    Policy,
    add_policy,
    get_expiring_soon,
    is_policy_duplicate,
    sort_policies_by_price,
)
from models.users import User


def _make_user_car() -> tuple[User, Car]:
    """Вспомогательная функция: создать пользователя и авто."""
    user = User(1, "Иванов Иван", "+7", "a@test.ru")
    car = Car(1, user, "А123БВ77", "Camry")
    return user, car


def _make_policy(
    policy_id: int = 1,
    price: float = 5000.0,
    end_date: date | None = None,
) -> Policy:
    """Вспомогательная функция: создать полис."""
    user, car = _make_user_car()
    if end_date is None:
        end_date = date.today() + timedelta(days=365)
    return Policy(
        policy_id, user, car, "Ингосстрах", "ОСАГО",
        date(2025, 1, 1), end_date, price,
    )


# ---------- Класс Policy ----------
def test_policy_creation():
    """Объект Policy создаётся с корректными атрибутами."""
    policy = _make_policy()
    assert policy.id == 1
    assert policy.policy_type == "ОСАГО"
    assert policy.user.full_name == "Иванов Иван"
    assert policy.car.license_plate == "А123БВ77"


def test_policy_str():
    """Строковое представление Policy содержит данные."""
    policy = _make_policy()
    text = str(policy)
    assert "ОСАГО" in text
    assert "А123БВ77" in text


def test_policy_from_data():
    """from_data создаёт Policy, связывая User и Car."""
    user, car = _make_user_car()
    data = {
        "id": 1,
        "user_id": 1,
        "car_id": 1,
        "company": "Ингосстрах",
        "policy_type": "ОСАГО",
        "start_date": "2025-01-01",
        "end_date": "2026-01-01",
        "price": 7500.0,
    }
    policy = Policy.from_data(data, [user], [car])
    assert policy is not None
    assert policy.user is user
    assert policy.car is car
    assert policy.price == 7500.0


# ---------- check_status ----------
def test_check_status_expired():
    """Полис в прошлом → 'истек'."""
    past = date.today() - timedelta(days=10)
    policy = _make_policy(end_date=past)
    assert policy.check_status() == "истек"


def test_check_status_active():
    """Полис в будущем → 'активен'."""
    future = date.today() + timedelta(days=365)
    policy = _make_policy(end_date=future)
    assert "активен" in policy.check_status()


# ---------- calculate_renewal_price ----------
def test_renewal_no_discount():
    """Без скидки цена не меняется."""
    policy = _make_policy(price=1000.0)
    assert policy.calculate_renewal_price(False, 30) == 1000.0


def test_renewal_with_discount():
    """Скидка 10% за безаварийность."""
    policy = _make_policy(price=1000.0)
    assert policy.calculate_renewal_price(True, 30) == 900.0


def test_renewal_young_driver():
    """Надбавка 30% для водителей младше 25."""
    policy = _make_policy(price=1000.0)
    assert policy.calculate_renewal_price(False, 22) == 1300.0


# ---------- Функции работы с коллекцией ----------
def test_add_policy():
    """add_policy добавляет объект в коллекцию."""
    user, car = _make_user_car()
    policies: list[Policy] = []
    policy = add_policy(
        policies, user, car, "Ингосстрах", "ОСАГО",
        date(2025, 1, 1), date(2026, 1, 1), 5000.0,
    )
    assert len(policies) == 1
    assert policy.id == 1


def test_is_policy_duplicate():
    """Дубликат по авто + типу полиса обнаруживается."""
    user, car = _make_user_car()
    policies: list[Policy] = []
    add_policy(
        policies, user, car, "Ингосстрах", "ОСАГО",
        date(2025, 1, 1), date(2026, 1, 1), 5000.0,
    )
    assert is_policy_duplicate(policies, car, "ОСАГО")
    assert not is_policy_duplicate(policies, car, "КАСКО")


def test_sort_policies_by_price():
    """Сортировка по цене (возрастание)."""
    p1 = _make_policy(policy_id=1, price=9000.0)
    p2 = _make_policy(policy_id=2, price=3000.0)
    p3 = _make_policy(policy_id=3, price=6000.0)
    result = sort_policies_by_price([p1, p2, p3])
    assert [p.price for p in result] == [3000.0, 6000.0, 9000.0]


def test_get_expiring_soon():
    """Полисы, истекающие в ближайшие 30 дней."""
    today = date.today()
    soon = _make_policy(policy_id=1, end_date=today + timedelta(days=10))
    far = _make_policy(policy_id=2, end_date=today + timedelta(days=100))
    expired = _make_policy(policy_id=3, end_date=today - timedelta(days=5))
    result = get_expiring_soon([soon, far, expired], days=30)
    assert len(result) == 1
    assert result[0].id == 1