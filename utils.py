"""Вспомогательные функции безопасного ввода с обработкой исключений."""

from datetime import date, datetime


def input_str(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[ERROR] Поле не может быть пустым.")


def input_int(prompt: str) -> int:
    """Запросить целое число."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("[ERROR] Введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить число (цену)."""
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if value < 0:
                print("[ERROR] Число не может быть отрицательным.")
                continue
            return value
        except ValueError:
            print("[ERROR] Введите число (например, 7500.50).")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("[ERROR] Неверный формат даты. Пример: 2026-09-17")