"""Тесты для модуля policies."""

from datetime import date, timedelta

from policies import (
    add_policy,
    calculate_renewal_price,
    check_policy_status,
    get_expiring_soon,
    is_policy_duplicate,
    sort_policies_by_price,
)


def test_check_policy_status_expired():
    """Полис в прошлом — 'истек'."""
    past = date.today() - timedelta(days=10)
    assert check_policy_status(past) == "истек"


def test_check_policy_status_active():
    """Полис в будущем — 'активен'."""
    future = date.today() + timedelta(days=365)
    assert "активен" in check_policy_status(future)


def test_calculate_renewal_price_no_discount():
    """Без скидок — цена не меняется."""
    assert calculate_renewal_price(1000.0, False, 30) == 1000.0


def test_calculate_renewal_price_with_discount():
    """Скидка за безаварийность."""
    assert calculate_renewal_price(1000.0, True, 30) == 900.0


def test_calculate_renewal_price_young_driver():
    """Надбавка для водителей младше 25."""
    assert calculate_renewal_price(1000.0, False, 22) == 1300.0


def test_add_policy_assigns_id():
    """add_policy присваивает ID и добавляет в список."""
    policies: list[dict] = []
    policy = add_policy(
        policies,
        user_id=1,
        car_id=1,
        company="Тест",
        policy_type="ОСАГО",
        start_date=date(2025, 1, 1),
        end_date=date(2026, 1, 1),
        price=5000.0,
    )
    assert len(policies) == 1
    assert policy["id"] == 1


def test_is_policy_duplicate():
    """Дубликат по авто + тип полиса обнаруживается."""
    policies = [{"car_id": 1, "policy_type": "ОСАГО"}]
    assert is_policy_duplicate(policies, 1, "ОСАГО")
    assert not is_policy_duplicate(policies, 1, "КАСКО")


def test_sort_policies_by_price():
    """Сортировка по цене."""
    policies = [
        {"id": 1, "price": 9000.0},
        {"id": 2, "price": 3000.0},
        {"id": 3, "price": 6000.0},
    ]
    result = sort_policies_by_price(policies)
    assert [p["price"] for p in result] == [3000.0, 6000.0, 9000.0]


def test_get_expiring_soon():
    """Истекающие в ближайшие 30 дней."""
    today = date.today()
    policies = [
        {"id": 1, "end_date": today + timedelta(days=10)},
        {"id": 2, "end_date": today + timedelta(days=100)},
        {"id": 3, "end_date": today - timedelta(days=5)},
    ]
    result = get_expiring_soon(policies, days=30)
    assert len(result) == 1
    assert result[0]["id"] == 1