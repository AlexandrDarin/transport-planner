"""View-функции приложения users_app."""

from django.http import HttpResponse

from homepage.views import page, _breadcrumbs
from storage import (
    load_routes, load_users, load_stops, load_trips,
)


def users_list(request):
    """Страница /users/ — список пользователей."""
    users = load_users("data/users.json")
    crumbs = _breadcrumbs([("Главная", "/"), ("Пользователи", None)])

    if not users:
        content = """
        <h1 class="mb-3">Пользователи</h1>
        <div class="alert alert-info">Пользователей пока нет.</div>
        """
        return HttpResponse(page(
            "Пользователи", content, active="users", breadcrumbs=crumbs
        ))

    total_age = sum(u.age for u in users)
    avg_age = round(total_age / len(users), 1)
    with_benefits = sum(1 for u in users if u.has_benefits)

    stats = f"""
    <div class="row g-3 mb-3">
        <div class="col-md-4">
            <div class="stat-card">
                <div class="stat-value">{len(users)}</div>
                <div class="stat-label">пользователей</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="stat-card">
                <div class="stat-value">{avg_age}</div>
                <div class="stat-label">средний возраст</div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="stat-card">
                <div class="stat-value">{with_benefits}</div>
                <div class="stat-label">со льготами</div>
            </div>
        </div>
    </div>
    """

    items = ""
    for u in users:
        badge = (
            '<span class="badge bg-warning text-dark">льготы</span>'
            if u.has_benefits
            else '<span class="badge bg-secondary">без льгот</span>'
        )
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<div>'
            f'<a href="/users/{u.id}/" '
            f'class="fw-bold text-decoration-none">{u.name}</a> '
            f'<span class="text-muted">· {u.age} лет</span>'
            f'</div>{badge}</li>'
        )

    content = f"""
    <h1 class="mb-3">Пользователи</h1>
    {stats}
    <ul class="list-group shadow-sm">{items}</ul>
    """
    return HttpResponse(page(
        "Пользователи", content, active="users", breadcrumbs=crumbs
    ))


def user_detail(request, user_id: int):
    """Страница /users/<id>/ — информация о пользователе."""
    users = load_users("data/users.json")
    user = next((u for u in users if u.id == user_id), None)

    crumbs = _breadcrumbs([
        ("Главная", "/"),
        ("Пользователи", "/users/"),
        (f"Пользователь {user_id}", None),
    ])

    if user is None:
        content = """
        <div class="alert alert-warning">
            <h1 class="h4 mb-0">Пользователь не найден</h1>
        </div>
        <a href="/users/" class="btn btn-outline-secondary">
            ← к списку пользователей
        </a>
        """
        return HttpResponse(
            page("Пользователь не найден", content,
                 active="users", breadcrumbs=crumbs),
            status=404,
        )

    routes = load_routes("data/routes.json")
    stops = load_stops("data/stops.json")
    trips = load_trips("data/trips.json", routes, users, stops)
    user_trips = [t for t in trips if t.user.id == user_id]

    active = [t for t in user_trips if not t.is_cancelled]
    total_price = sum(t.calculate_price() for t in active)

    trips_html = ""
    if user_trips:
        for t in user_trips:
            state = "отменена" if t.is_cancelled else "активна"
            badge = "bg-secondary" if t.is_cancelled else "bg-success"
            trips_html += (
                f'<li class="list-group-item d-flex '
                f'justify-content-between align-items-center">'
                f'<a href="/trips/{t.id}/">Поездка №{t.id} · '
                f'{t.route.number} · {t.date}</a>'
                f'<span class="badge {badge}">{state}</span></li>'
            )
    else:
        trips_html = (
            '<li class="list-group-item text-muted">'
            'У пользователя пока нет поездок.</li>'
        )

    benefits = "есть" if user.has_benefits else "нет"

    content = f"""
    <div class="card shadow-sm mb-4">
        <div class="card-body">
            <h5 class="card-title mb-3">{user.name}</h5>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>ID:</strong> {user.id}</p>
                    <p><strong>Возраст:</strong> {user.age} лет</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Льготы:</strong> {benefits}</p>
                    <p>
                        <strong>Скидка:</strong>
                        {int((1 - user.get_discount()) * 100)}%
                    </p>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <div class="stat-card">
                        <div class="stat-value">{len(user_trips)}</div>
                        <div class="stat-label">всего поездок</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stat-card">
                        <div class="stat-value text-success">
                            {len(active)}
                        </div>
                        <div class="stat-label">активных</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stat-card">
                        <div class="stat-value">
                            {total_price:.0f} руб.
                        </div>
                        <div class="stat-label">стоимость активных</div>
                    </div>
                </div>
            </div>
            <a href="/users/" class="btn btn-outline-secondary mt-3">
                ← к списку пользователей
            </a>
        </div>
    </div>

    <h6 class="mb-2">Поездки пользователя</h6>
    <ul class="list-group shadow-sm">{trips_html}</ul>
    """
    return HttpResponse(page(
        user.name, content, active="users", breadcrumbs=crumbs
    ))