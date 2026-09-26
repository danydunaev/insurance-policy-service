"""Класс Car и функции работы с автомобилями."""

from models.users import User


class Car:
    """Автомобиль, привязанный к владельцу."""

    def __init__(
        self,
        car_id: int,
        owner: User,
        license_plate: str,
        model: str,
    ) -> None:
        """Создать объект автомобиля."""
        self.id = car_id
        self.owner = owner
        self.license_plate = license_plate.upper()
        self.model = model

    def __str__(self) -> str:
        """Строковое представление автомобиля."""
        return f"[{self.id}] {self.license_plate} ({self.model}) — {self.owner.full_name}"

    @classmethod
    def from_data(cls, data: dict, users: list[User]) -> "Car | None":
        """Создать Car из словаря, найдя владельца в коллекции."""
        owner = next((u for u in users if u.id == data["owner_id"]), None)
        if owner is None:
            return None
        return cls(
            car_id=data["id"],
            owner=owner,
            license_plate=data["license_plate"],
            model=data["model"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "owner_id": self.owner.id,
            "license_plate": self.license_plate,
            "model": self.model,
        }


def _next_id(cars: list[Car]) -> int:
    """Следующий свободный ID."""
    if not cars:
        return 1
    return max(c.id for c in cars) + 1


def add_car(
    cars: list[Car],
    owner: User,
    license_plate: str,
    model: str,
) -> Car:
    """Создать объект Car и добавить его в коллекцию."""
    car = Car(_next_id(cars), owner, license_plate, model)
    cars.append(car)
    return car


def find_car_by_plate(cars: list[Car], plate: str) -> Car | None:
    """Найти автомобиль по госномеру."""
    plate_upper = plate.upper()
    for car in cars:
        if car.license_plate == plate_upper:
            return car
    return None


def get_cars_by_owner(cars: list[Car], owner: User) -> list[Car]:
    """Все автомобили конкретного владельца."""
    return [c for c in cars if c.owner.id == owner.id]