"""Загрузка и сохранение данных проекта в JSON-файлах.

Преобразует JSON ↔ объекты классов User, Car, Policy.
"""

import json
import os

from models.cars import Car
from models.policies import Policy
from models.users import User


def _ensure_dir(filename: str) -> None:
    """Создать папку для файла, если её нет."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)


# ---------- Пользователи ----------
def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return [User.from_data(item) for item in data]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [u.to_data() for u in users],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"[ERROR] Не удалось сохранить {filename}: {error}")


# ---------- Автомобили ----------
def load_cars(filename: str, users: list[User]) -> list[Car]:
    """Загрузить автомобили из JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    result = []
    for item in data:
        car = Car.from_data(item, users)
        if car is not None:
            result.append(car)
    return result


def save_cars(filename: str, cars: list[Car]) -> None:
    """Сохранить автомобили в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [c.to_data() for c in cars],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"[ERROR] Не удалось сохранить {filename}: {error}")


# ---------- Полисы ----------
def load_policies(
    filename: str,
    users: list[User],
    cars: list[Car],
) -> list[Policy]:
    """Загрузить полисы из JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    result = []
    for item in data:
        policy = Policy.from_data(item, users, cars)
        if policy is not None:
            result.append(policy)
    return result


def save_policies(filename: str, policies: list[Policy]) -> None:
    """Сохранить полисы в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [p.to_data() for p in policies],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"[ERROR] Не удалось сохранить {filename}: {error}")