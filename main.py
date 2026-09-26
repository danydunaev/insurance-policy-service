"""Главный модуль: меню приложения и работа с объектами."""

from models.cars import add_car, find_car_by_plate, get_cars_by_owner
from models.policies import (
    add_policy,
    find_policies_by_user,
    get_expiring_soon,
    is_policy_duplicate,
    sort_policies_by_price,
)
from models.users import add_user, find_user_by_name, get_user_by_id
from storage import (
    load_cars,
    load_policies,
    load_users,
    save_cars,
    save_policies,
    save_users,
)
from utils import input_date, input_float, input_int, input_str

USERS_FILE = "data/users.json"
CARS_FILE = "data/cars.json"
POLICIES_FILE = "data/policies.json"


# ---------- Вывод ----------
def show_users(users: list) -> None:
    """Показать всех пользователей."""
    if not users:
        print("\n[INFO] Пользователей нет.")
        return
    print("\n" + "-" * 70)
    for user in users:
        print(user)
    print("-" * 70)


def show_cars(cars: list) -> None:
    """Показать все автомобили."""
    if not cars:
        print("\n[INFO] Автомобилей нет.")
        return
    print("\n" + "-" * 70)
    for car in cars:
        print(car)
    print("-" * 70)


def show_policies(policies: list) -> None:
    """Показать все полисы."""
    if not policies:
        print("\n[INFO] Полисов нет.")
        return
    print("\n" + "-" * 110)
    print(f"{'ID':<4} {'Владелец':<25} {'Авто':<12} {'Тип':<8} "
          f"{'Компания':<15} {'Цена':>9} {'Статус':<20}")
    print("-" * 110)
    for policy in policies:
        print(f"{policy.id:<4} {policy.user.full_name:<25} "
              f"{policy.car.license_plate:<12} {policy.policy_type:<8} "
              f"{policy.company:<15} {policy.price:>9.2f} "
              f"{policy.check_status():<20}")
    print("-" * 110)


# ---------- Действия меню ----------
def action_add_user(users: list) -> None:
    """Добавить пользователя."""
    print("\n--- Новый пользователь ---")
    full_name = input_str("ФИО: ")
    phone = input_str("Телефон: ")
    email = input_str("Email: ")
    user = add_user(users, full_name, phone, email)
    print(f"[OK] Пользователь создан. ID={user.id}")


def action_add_car(cars: list, users: list) -> None:
    """Добавить автомобиль."""
    print("\n--- Новый автомобиль ---")
    show_users(users)
    if not users:
        print("[INFO] Сначала добавьте пользователя.")
        return
    owner_id = input_int("ID владельца: ")
    owner = get_user_by_id(users, owner_id)
    if owner is None:
        print(f"[ERROR] Пользователь с ID={owner_id} не найден.")
        return
    plate = input_str("Госномер: ")
    model = input_str("Марка/модель: ")
    car = add_car(cars, owner, plate, model)
    print(f"[OK] Автомобиль создан. ID={car.id}")


def action_add_policy(cars: list, users: list, policies: list) -> None:
    """Добавить полис."""
    print("\n--- Новый полис ---")
    show_users(users)
    if not users:
        print("[INFO] Сначала добавьте пользователя.")
        return
    user_id = input_int("ID владельца: ")
    user = get_user_by_id(users, user_id)
    if user is None:
        print(f"[ERROR] Пользователь с ID={user_id} не найден.")
        return

    user_cars = get_cars_by_owner(cars, user)
    if not user_cars:
        print("[INFO] У пользователя нет автомобилей.")
        return
    print("\nАвтомобили владельца:")
    for car in user_cars:
        print(f"  {car}")
    car_id = input_int("ID автомобиля: ")
    car = next((c for c in user_cars if c.id == car_id), None)
    if car is None:
        print(f"[ERROR] Автомобиль с ID={car_id} не найден у владельца.")
        return

    policy_type = input_str("Тип полиса (ОСАГО/КАСКО): ").upper()
    if is_policy_duplicate(policies, car, policy_type):
        print("[ERROR] Такой полис для этого автомобиля уже существует.")
        return

    company = input_str("Страховая компания: ")
    start_date = input_date("Дата начала (ГГГГ-ММ-ДД): ")
    end_date = input_date("Дата окончания (ГГГГ-ММ-ДД): ")
    price = input_float("Стоимость: ")

    policy = add_policy(
        policies, user, car, company,
        policy_type, start_date, end_date, price,
    )
    print(f"[OK] Полис создан. ID={policy.id}")


def action_find_user(users: list) -> None:
    """Найти пользователей по ФИО."""
    print("\n--- Поиск пользователя ---")
    query = input_str("Введите ФИО или часть: ")
    found = find_user_by_name(users, query)
    if not found:
        print("[INFO] Ничего не найдено.")
        return
    for user in found:
        print(f"  {user}")


def action_policies_by_user(users: list, policies: list) -> None:
    """Показать полисы конкретного пользователя."""
    print("\n--- Полисы пользователя ---")
    user_id = input_int("ID пользователя: ")
    user = get_user_by_id(users, user_id)
    if user is None:
        print(f"[ERROR] Пользователь с ID={user_id} не найден.")
        return
    found = find_policies_by_user(policies, user)
    show_policies(found)


def action_check_status(policies: list) -> None:
    """Показать статус полиса."""
    print("\n--- Статус полиса ---")
    policy_id = input_int("ID полиса: ")
    policy = next((p for p in policies if p.id == policy_id), None)
    if policy is None:
        print(f"[ERROR] Полис с ID={policy_id} не найден.")
        return
    print(f"Дата окончания: {policy.end_date}")
    print(f"Статус: {policy.check_status()}")


def action_renewal_price(policies: list) -> None:
    """Рассчитать стоимость продления."""
    print("\n--- Расчёт продления ---")
    policy_id = input_int("ID полиса: ")
    policy = next((p for p in policies if p.id == policy_id), None)
    if policy is None:
        print(f"[ERROR] Полис с ID={policy_id} не найден.")
        return
    is_free = input_str("Безаварийная езда? (да/нет): ").lower() in ("да", "yes", "y")
    age = input_int("Возраст водителя: ")
    new_price = policy.calculate_renewal_price(is_free, age)
    print(f"Базовая цена:   {policy.price:.2f} руб.")
    print(f"Цена продления: {new_price:.2f} руб.")


def action_expiring(policies: list) -> None:
    """Истекающие в ближайшие 30 дней."""
    print("\n--- Истекающие в ближайшие 30 дней ---")
    show_policies(get_expiring_soon(policies, days=30))


def action_sort(policies: list) -> None:
    """Полисы, отсортированные по цене."""
    print("\n--- Полисы по цене (возрастание) ---")
    show_policies(sort_policies_by_price(policies))


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
    cars = load_cars(CARS_FILE, users)
    policies = load_policies(POLICIES_FILE, users, cars)

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
            show_cars(cars)
        elif choice == 4:
            action_add_car(cars, users)
        elif choice == 5:
            show_policies(policies)
        elif choice == 6:
            action_add_policy(cars, users, policies)
        elif choice == 7:
            action_find_user(users)
        elif choice == 8:
            action_policies_by_user(users, policies)
        elif choice == 9:
            action_check_status(policies)
        elif choice == 10:
            action_renewal_price(policies)
        elif choice == 11:
            action_expiring(policies)
        elif choice == 12:
            action_sort(policies)
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