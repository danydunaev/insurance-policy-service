"""Тесты для модуля cars."""

from cars import add_car, find_car_by_plate, get_cars_by_owner


def test_add_car():
    """add_car добавляет запись с ID."""
    cars: dict[int, dict] = {}
    car = add_car(cars, owner_id=1, license_plate="а123бв77", model="Camry")
    assert len(cars) == 1
    assert car["id"] == 1
    assert car["license_plate"] == "А123БВ77"  # приведение к верхнему регистру


def test_find_car_by_plate():
    """Поиск по госномеру (без учёта регистра)."""
    cars: dict[int, dict] = {}
    add_car(cars, 1, "А123БВ77", "Camry")
    assert find_car_by_plate(cars, "а123бв77") is not None
    assert find_car_by_plate(cars, "X000XX00") is None


def test_get_cars_by_owner():
    """Все машины конкретного владельца."""
    cars: dict[int, dict] = {}
    add_car(cars, 1, "А111АА11", "Camry")
    add_car(cars, 1, "Б222ББ22", "Corolla")
    add_car(cars, 2, "В333ВВ33", "Focus")
    owner1_cars = get_cars_by_owner(cars, 1)
    assert len(owner1_cars) == 2
    assert all(c["owner_id"] == 1 for c in owner1_cars)