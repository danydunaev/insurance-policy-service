"""View-функции для отображения полисов."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_cars, load_policies, load_users

USERS_FILE = "data/users.json"
CARS_FILE = "data/cars.json"
POLICIES_FILE = "data/policies.json"


def policies_list(request) -> HttpResponse:
    """Страница со списком всех полисов."""
    users = load_users(USERS_FILE)
    cars = load_cars(CARS_FILE, users)
    policies = load_policies(POLICIES_FILE, users, cars)

    if not policies:
        content = """
        <h1>Полисы</h1>
        <p class="text-muted">Список полисов пуст.</p>
        """
        return HttpResponse(page("Полисы", content))

    items = ""
    for policy in policies:
        status = policy.check_status()
        if "истек" in status:
            badge = "bg-danger"
        elif "истекает" in status:
            badge = "bg-warning text-dark"
        else:
            badge = "bg-success"

        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/policies/{policy.id}/">
                {policy.user.full_name} — {policy.car.license_plate}
                ({policy.policy_type})
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <h1>Полисы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Полисы", content))


def policy_detail(request, policy_id: int) -> HttpResponse:
    """Страница конкретного полиса."""
    users = load_users(USERS_FILE)
    cars = load_cars(CARS_FILE, users)
    policies = load_policies(POLICIES_FILE, users, cars)

    policy = next((p for p in policies if p.id == policy_id), None)

    if policy is None:
        content = """
        <h1 class="text-danger">Полис не найден</h1>
        <a href="/policies/" class="btn btn-outline-secondary">
            ← к списку полисов
        </a>
        """
        return HttpResponse(
            page("Полис не найден", content),
            status=404,
        )

    status = policy.check_status()
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Полис №{policy.id}</h5>
            <p class="card-text">
                <strong>Владелец:</strong> {policy.user.full_name}
            </p>
            <p class="card-text">
                <strong>Автомобиль:</strong>
                {policy.car.license_plate} ({policy.car.model})
            </p>
            <p class="card-text">
                <strong>Компания:</strong> {policy.company}
            </p>
            <p class="card-text">
                <strong>Тип:</strong> {policy.policy_type}
            </p>
            <p class="card-text">
                <strong>Период:</strong>
                {policy.start_date} — {policy.end_date}
            </p>
            <p class="card-text">
                <strong>Стоимость:</strong> {policy.price:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Статус:</strong> {status}
            </p>
            <a href="/policies/" class="btn btn-outline-secondary">
                ← к списку полисов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Полис №{policy.id}", content))