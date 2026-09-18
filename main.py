"""Главный модуль: меню приложения и вызов функций из модулей."""

from users import add_user, find_user_by_name, get_user_by_id
from cars import add_car, find_car_by_plate, get_cars_by_owner
from policies import (
    add_policy,
    calculate_renewal_price,
    check_policy_status,
    find_policies_by_user,
    get_expiring_soon,
    is_policy_duplicate,
    sort_policies_by_price,
)
from storage import (
    load_users, save_users,
    load_cars, save_cars,
    load_policies, save_policies,
)
from utils import input_str, input_int, input_float, input_date

USERS_FILE = "data/users.json"
CARS_FILE = "data/cars.json"
POLICIES_FILE = "data/policies.json"


# ---------- Вывод ----------
def show_users(users: dict) -> None:
    """Показать всех пользователей."""
    if not users:
        print("\n[INFO] Пользователей нет.")
        return
    print("\n" + "-" * 70)
    print(f"{'ID':<4} {'ФИО':<30} {'Телефон':<18} {'Email':<20}")
    print("-" * 70)
    for user_id, user in users.items():
        print(f"{user.get('id', user_id):<4} "
              f"{user.get('full_name', '—'):<30} "
              f"{user.get('phone', '—'):<18} "
              f"{user.get('email', '—'):<20}")
    print("-" * 70)


def show_cars(cars: dict, users: dict) -> None:
    """Показать все автомобили."""
    if not cars:
        print("\n[INFO] Автомобилей нет.")
        return
    print("\n" + "-" * 80)
    print(f"{'ID':<4} {'Госномер':<12} {'Модель':<25} {'Владелец':<30}")
    print("-" * 80)
    for car_id, car in cars.items():
        owner = users.get(car.get("owner_id"), {})
        owner_name = owner.get("full_name", "—")
        print(f"{car.get('id', car_id):<4} "
              f"{car.get('license_plate', '—'):<12} "
              f"{car.get('model', '—'):<25} "
              f"{owner_name:<30}")
    print("-" * 80)


def show_policies(policies: list[dict], users: dict, cars: dict) -> None:
    """Показать все полисы в виде таблицы."""
    if not policies:
        print("\n[INFO] Полисов нет.")
        return
    print("\n" + "-" * 110)
    print(f"{'ID':<4} {'Владелец':<22} {'Авто':<10} {'Тип':<8} "
          f"{'Компания':<15} {'Цена':>9} {'Статус':<20}")
    print("-" * 110)
    for policy in policies:
        user = users.get(policy.get("user_id"), {})
        car = cars.get(policy.get("car_id"), {})
        try:
            status = check_policy_status(policy.get("end_date"))
        except (AttributeError, TypeError):
            status = "—"
        price = policy.get("price", 0)
        print(f"{policy.get('id', '—'):<4} "
              f"{user.get('full_name', '—'):<22} "
              f"{car.get('license_plate', '—'):<10} "
              f"{policy.get('policy_type', '—'):<8} "
              f"{policy.get('company', '—'):<15} "
              f"{price:>9.2f} "
              f"{status:<20}")
    print("-" * 110)


# ---------- Действия меню ----------
def action_add_user(users: dict) -> None:
    """Добавить пользователя."""
    print("\n--- Новый пользователь ---")
    full_name = input_str("ФИО: ")
    phone = input_str("Телефон: ")
    email = input_str("Email: ")
    user = add_user(users, full_name, phone, email)
    print(f"[OK] Пользователь создан. ID={user['id']}")


def action_add_car(users: dict, cars: dict) -> None:
    """Добавить автомобиль."""
    print("\n--- Новый автомобиль ---")
    show_users(users)
    if not users:
        print("[INFO] Сначала добавьте пользователя.")
        return
    owner_id = input_int("ID владельца: ")
    if get_user_by_id(users, owner_id) is None:
        print(f"[ERROR] Пользователь с ID={owner_id} не найден.")
        return
    plate = input_str("Госномер: ")
    model = input_str("Марка/модель: ")
    car = add_car(cars, owner_id, plate, model)
    print(f"[OK] Автомобиль создан. ID={car['id']}")


def action_add_policy(users: dict, cars: dict, policies: list[dict]) -> None:
    """Добавить полис."""
    print("\n--- Новый полис ---")
    show_users(users)
    if not users:
        print("[INFO] Сначала добавьте пользователя.")
        return
    user_id = input_int("ID владельца: ")
    if get_user_by_id(users, user_id) is None:
        print(f"[ERROR] Пользователь с ID={user_id} не найден.")
        return

    user_cars = get_cars_by_owner(cars, user_id)
    if not user_cars:
        print("[INFO] У пользователя нет автомобилей.")
        return
    print("\nАвтомобили владельца:")
    for car in user_cars:
        print(f"  ID={car['id']} — {car['license_plate']} ({car['model']})")
    car_id = input_int("ID автомобиля: ")
    if not any(c["id"] == car_id for c in user_cars):
        print(f"[ERROR] Автомобиль с ID={car_id} не найден у владельца.")
        return

    policy_type = input_str("Тип полиса (ОСАГО/КАСКО): ").upper()
    if is_policy_duplicate(policies, car_id, policy_type):
        print("[ERROR] Такой полис для этого автомобиля уже существует.")
        return

    company = input_str("Страховая компания: ")
    start_date = input_date("Дата начала (ГГГГ-ММ-ДД): ")
    end_date = input_date("Дата окончания (ГГГГ-ММ-ДД): ")
    price = input_float("Стоимость: ")

    policy = add_policy(
        policies, user_id, car_id, company,
        policy_type, start_date, end_date, price,
    )
    print(f"[OK] Полис создан. ID={policy['id']}")


def action_find_user(users: dict) -> None:
    """Найти пользователей по ФИО."""
    print("\n--- Поиск пользователя ---")
    query = input_str("Введите ФИО или часть: ")
    found = find_user_by_name(users, query)
    if not found:
        print("[INFO] Ничего не найдено.")
        return
    for user in found:
        print(f"  ID={user.get('id', '—')} — "
              f"{user.get('full_name', '—')}, "
              f"{user.get('phone', '—')}")


def action_policies_by_user(users: dict, cars: dict, policies: list[dict]) -> None:
    """Показать полисы конкретного пользователя."""
    print("\n--- Полисы пользователя ---")
    user_id = input_int("ID пользователя: ")
    if get_user_by_id(users, user_id) is None:
        print(f"[ERROR] Пользователь с ID={user_id} не найден.")
        return
    found = find_policies_by_user(policies, user_id)
    show_policies(found, users, cars)


def action_check_status(policies: list[dict]) -> None:
    """Показать статус полиса по ID."""
    print("\n--- Статус полиса ---")
    policy_id = input_int("ID полиса: ")
    policy = next((p for p in policies if p.get("id") == policy_id), None)
    if policy is None:
        print(f"[ERROR] Полис с ID={policy_id} не найден.")
        return
    print(f"Дата окончания: {policy.get('end_date', '—')}")
    try:
        status = check_policy_status(policy.get("end_date"))
    except (AttributeError, TypeError):
        status = "—"
    print(f"Статус: {status}")


def action_renewal_price(policies: list[dict]) -> None:
    """Рассчитать стоимость продления."""
    print("\n--- Расчёт продления ---")
    policy_id = input_int("ID полиса: ")
    policy = next((p for p in policies if p.get("id") == policy_id), None)
    if policy is None:
        print(f"[ERROR] Полис с ID={policy_id} не найден.")
        return
    is_free = input_str("Безаварийная езда? (да/нет): ").lower() in ("да", "yes", "y")
    age = input_int("Возраст водителя: ")
    new_price = calculate_renewal_price(policy.get("price", 0), is_free, age)
    print(f"Базовая цена:   {policy.get('price', 0):.2f} руб.")
    print(f"Цена продления: {new_price:.2f} руб.")


def action_expiring(users: dict, cars: dict, policies: list[dict]) -> None:
    """Полисы, истекающие в ближайшие 30 дней."""
    print("\n--- Истекающие в ближайшие 30 дней ---")
    show_policies(get_expiring_soon(policies, days=30), users, cars)


def action_sort(users: dict, cars: dict, policies: list[dict]) -> None:
    """Полисы, отсортированные по цене."""
    print("\n--- Полисы по цене (возрастание) ---")
    show_policies(sort_policies_by_price(policies), users, cars)


# ---------- Меню ----------
def print_menu() -> None:
    """Показать пункты меню."""
    print("\n" + "=" * 50)
    print("СЕРВИС УЧЁТА СТРАХОВЫХ ПОЛИСОВ")
    print("=" * 50)
    print("1.  Показать всех пользователей")
    print("2.  Добавить пользователя")
    print("3.  Показать все автомобили")
    print("4.  Добавить автомобиль")
    print("5.  Показать все полисы")
    print("6.  Добавить полис")
    print("7.  Найти пользователя по ФИО")
    print("8.  Полисы конкретного пользователя")
    print("9.  Проверить статус полиса")
    print("10. Рассчитать стоимость продления")
    print("11. Истекающие в ближайшие 30 дней")
    print("12. Полисы по цене (сортировка)")
    print("0.  Сохранить и выйти")
    print("=" * 50)


def main() -> None:
    """Точка входа приложения."""
    users = load_users(USERS_FILE)
    cars = load_cars(CARS_FILE)
    policies = load_policies(POLICIES_FILE)

    print(f"[INFO] Загружено: пользователей — {len(users)}, "
          f"автомобилей — {len(cars)}, полисов — {len(policies)}")

    while True:
        print_menu()
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_users(users)
        elif choice == 2:
            action_add_user(users)
        elif choice == 3:
            show_cars(cars, users)
        elif choice == 4:
            action_add_car(users, cars)
        elif choice == 5:
            show_policies(policies, users, cars)
        elif choice == 6:
            action_add_policy(users, cars, policies)
        elif choice == 7:
            action_find_user(users)
        elif choice == 8:
            action_policies_by_user(users, cars, policies)
        elif choice == 9:
            action_check_status(policies)
        elif choice == 10:
            action_renewal_price(policies)
        elif choice == 11:
            action_expiring(users, cars, policies)
        elif choice == 12:
            action_sort(users, cars, policies)
        elif choice == 0:
            save_users(USERS_FILE, users)
            save_cars(CARS_FILE, cars)
            save_policies(POLICIES_FILE, policies)
            print("\n[OK] Данные сохранены. До свидания!")
            break
        else:
            print("\n[ERROR] Неверный пункт меню.")


if __name__ == "__main__":
    main()