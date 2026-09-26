"""Тесты для моделей автомобилей."""

from models.cars import Car, add_car, find_car_by_plate, get_cars_by_owner
from models.users import User


def _make_owner(owner_id: int = 1) -> User:
    """Вспомогательная функция: создать владельца."""
    return User(owner_id, "Иванов Иван", "+7", "a@test.ru")


def test_car_creation():
    """Объект Car создаётся с корректными атрибутами."""
    owner = _make_owner()
    car = Car(1, owner, "а123бв77", "Camry")
    assert car.id == 1
    assert car.license_plate == "А123БВ77"  # нормализовано
    assert car.model == "Camry"
    assert car.owner is owner


def test_car_str():
    """Строковое представление Car содержит данные."""
    car = Car(1, _make_owner(), "А123БВ77", "Camry")
    text = str(car)
    assert "А123БВ77" in text
    assert "Camry" in text


def test_car_from_data():
    """from_data находит владельца и создаёт Car."""
    owner = _make_owner()
    data = {
        "id": 1,
        "owner_id": 1,
        "license_plate": "А123БВ77",
        "model": "Camry",
    }
    car = Car.from_data(data, [owner])
    assert car is not None
    assert car.owner is owner


def test_add_car():
    """add_car добавляет объект в коллекцию."""
    cars: list[Car] = []
    car = add_car(cars, _make_owner(), "А111АА11", "Camry")
    assert len(cars) == 1
    assert car.id == 1


def test_find_car_by_plate():
    """Поиск по госномеру не зависит от регистра."""
    cars: list[Car] = []
    add_car(cars, _make_owner(), "А123БВ77", "Camry")
    assert find_car_by_plate(cars, "а123бв77") is not None
    assert find_car_by_plate(cars, "X000XX00") is None


def test_get_cars_by_owner():
    """Возвращает только авто нужного владельца."""
    owner1 = _make_owner(1)
    owner2 = _make_owner(2)
    cars: list[Car] = []
    add_car(cars, owner1, "А111АА11", "Camry")
    add_car(cars, owner1, "Б222ББ22", "Corolla")
    add_car(cars, owner2, "В333ВВ33", "Focus")
    result = get_cars_by_owner(cars, owner1)
    assert len(result) == 2