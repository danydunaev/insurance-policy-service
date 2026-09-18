"""Работа с автомобилями."""


def _next_id(cars: dict[int, dict]) -> int:
    """Вернуть следующий свободный ID."""
    if not cars:
        return 1
    return max(cars.keys()) + 1


def add_car(
    cars: dict[int, dict],
    owner_id: int,
    license_plate: str,
    model: str,
) -> dict:
    """Добавить автомобиль. Возвращает созданную запись."""
    car_id = _next_id(cars)
    car = {
        "id": car_id,
        "owner_id": owner_id,
        "license_plate": license_plate.upper(),
        "model": model,
    }
    cars[car_id] = car
    return car


def find_car_by_plate(cars: dict[int, dict], plate: str) -> dict | None:
    """Найти автомобиль по госномеру."""
    plate_upper = plate.upper()
    for car in cars.values():
        if car["license_plate"] == plate_upper:
            return car
    return None


def get_cars_by_owner(cars: dict[int, dict], owner_id: int) -> list[dict]:
    """Вернуть все автомобили конкретного владельца."""
    return [car for car in cars.values() if car["owner_id"] == owner_id]