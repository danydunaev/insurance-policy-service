"""Загрузка и сохранение данных проекта в JSON-файлах.

Даты хранятся как строки ISO, при загрузке преобразуются в date.
"""

import json
import os
from datetime import date


# ---------- Пользователи ----------
def load_users(filename: str) -> dict[int, dict]:
    """Загрузить пользователей из JSON. Ключ — ID (int)."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}
    return {int(k): v for k, v in data.items()}


def save_users(filename: str, users: dict[int, dict]) -> None:
    """Сохранить пользователей в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"[ERROR] Не удалось сохранить {filename}: {error}")


# ---------- Автомобили ----------
def load_cars(filename: str) -> dict[int, dict]:
    """Загрузить автомобили из JSON."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}
    return {int(k): v for k, v in data.items()}


def save_cars(filename: str, cars: dict[int, dict]) -> None:
    """Сохранить автомобили в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(cars, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"[ERROR] Не удалось сохранить {filename}: {error}")


# ---------- Полисы ----------
def _date_to_str(policy: dict) -> dict:
    """Преобразовать даты в строки для JSON."""
    item = policy.copy()
    for field in ("start_date", "end_date"):
        if isinstance(item.get(field), date):
            item[field] = item[field].isoformat()
    return item


def _str_to_date(policy: dict) -> dict:
    """Преобразовать строки обратно в date."""
    item = policy.copy()
    for field in ("start_date", "end_date"):
        if isinstance(item.get(field), str):
            try:
                item[field] = date.fromisoformat(item[field])
            except ValueError:
                pass
    return item


def load_policies(filename: str) -> list[dict]:
    """Загрузить список полисов из JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return [_str_to_date(p) for p in data]


def save_policies(filename: str, policies: list[dict]) -> None:
    """Сохранить полисы в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [_date_to_str(p) for p in policies],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"[ERROR] Не удалось сохранить {filename}: {error}")


def _ensure_dir(filename: str) -> None:
    """Создать папку для файла, если её нет."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)