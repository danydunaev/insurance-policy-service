"""
Начальный сценарий сервиса учета страховых полисов.
Реализует 3 функции согласно README.md:
1. Добавление нового полиса (имитация).
2. Проверка срока действия полиса.
3. Расчет стоимости продления полиса.
"""

from datetime import date, timedelta


# ---------- Функция 1: Добавление нового полиса (имитация) ----------
def create_policy(owner_name: str, car_number: str, company: str,
                  policy_type: str, start_date: date, end_date: date,
                  price: float) -> dict:
    """
    Создает словарь с данными нового полиса.
    В будущем будет сохранять данные в базу данных.
    """
    policy = {
        "owner_name": owner_name,
        "car_number": car_number,
        "company": company,
        "policy_type": policy_type,
        "start_date": start_date,
        "end_date": end_date,
        "price": price,
    }
    print(f"[CREATE] Полис для {owner_name} на авто {car_number} создан.")
    return policy


# ---------- Функция 2: Проверка срока действия полиса ----------
def check_policy_status(end_date: date) -> str:
    """
    Проверяет статус полиса относительно текущей даты.
    Возвращает строку: 'активен', 'истекает', 'истек'.
    """
    today = date.today()
    days_left = (end_date - today).days

    if days_left < 0:
        return "истек"
    elif days_left <= 30:
        return f"истекает (осталось {days_left} дней)"
    else:
        return f"активен (осталось {days_left} дней)"


# ---------- Функция 3: Расчет стоимости продления ----------
def calculate_renewal_price(base_price: float, is_accident_free: bool,
                            driver_age: int) -> float:
    """
    Рассчитывает стоимость продления полиса с учетом коэффициентов.
    :param base_price: базовая стоимость полиса
    :param is_accident_free: безаварийная езда (True/False)
    :param driver_age: возраст водителя
    :return: итоговая стоимость
    """
    price = base_price

    # Коэффициент за безаварийность (скидка 10%)
    if is_accident_free:
        price *= 0.9
        print("Применена скидка за безаварийность: -10%")

    # Коэффициент по возрасту (молодым водителям дороже)
    if driver_age < 25:
        price *= 1.3
        print("Применен коэффициент для водителей младше 25 лет: +30%")

    return round(price, 2)


# ---------- Основной сценарий ----------
if __name__ == "__main__":
    print("=" * 50)
    print("СЕРВИС УЧЕТА СТРАХОВЫХ ПОЛИСОВ")
    print("=" * 50)

    # 1. Создаем полис
    policy = create_policy(
        owner_name="Иванов Иван Иванович",
        car_number="А123БВ77",
        company="Ингосстрах",
        policy_type="ОСАГО",
        start_date=date(2025, 1, 1),
        end_date=date(2026, 1, 1),
        price=7500.0
    )

    # 2. Проверяем статус
    print(f"\nСтатус полиса: {check_policy_status(policy['end_date'])}")

    # 3. Рассчитываем стоимость продления
    print("\n--- Расчет стоимости продления ---")
    new_price = calculate_renewal_price(
        base_price=policy['price'],
        is_accident_free=True,
        driver_age=30
    )
    print(f"Базовая цена: {policy['price']} руб.")
    print(f"Цена продления: {new_price} руб.")