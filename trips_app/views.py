"""View-функции приложения trips_app."""

from django.http import HttpResponse

from homepage.views import page, _breadcrumbs
from storage import (
    load_routes, load_users, load_stops, load_trips,
)


def _load_trips():
    routes = load_routes("data/routes.json")
    users = load_users("data/users.json")
    stops = load_stops("data/stops.json")
    return load_trips("data/trips.json", routes, users, stops)


def trips_list(request):
    """Страница /trips/ — список поездок."""
    trips = _load_trips()

    crumbs = _breadcrumbs([("Главная", "/"), ("Поездки", None)])

    if not trips:
        content = """
        <h1 class="mb-3">Поездки</h1>
        <div class="alert alert-info">
            Поездок пока нет. Создать поездку можно через
            консольное приложение:
        </div>
        <pre class="bg-white p-3 border rounded">python main.py</pre>
        """
        return HttpResponse(page(
            "Поездки", content, active="trips", breadcrumbs=crumbs
        ))

    active = sum(1 for t in trips if not t.is_cancelled)
    cancelled = sum(1 for t in trips if t.is_cancelled)

    stats = f"""
    <div class="row g-3 mb-3">
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-value">{len(trips)}</div>
                <div class="stat-label">всего поездок</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-value text-success">{active}</div>
                <div class="stat-label">активных</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-value text-secondary">{cancelled}</div>
                <div class="stat-label">отменённых</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-value">
                    {sum(t.calculate_price() for t in trips if not t.is_cancelled):.0f}
                </div>
                <div class="stat-label">стоимость активных, руб.</div>
            </div>
        </div>
    </div>
    """

    items = ""
    for t in trips:
        state = "отменена" if t.is_cancelled else "активна"
        badge = "bg-secondary" if t.is_cancelled else "bg-success"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<div>'
            f'<a href="/trips/{t.id}/" '
            f'class="fw-bold text-decoration-none">№{t.id}</a> '
            f'<span class="text-muted">·</span> '
            f'<a href="/routes/{t.route.id}/" '
            f'class="text-decoration-none">{t.route.number}</a> '
            f'<span class="text-muted">·</span> '
            f'<span>{t.date}</span> '
            f'<span class="text-muted">·</span> '
            f'<span>{t.user.name}</span>'
            f'</div>'
            f'<span class="badge {badge}">{state}</span>'
            f'</li>'
        )

    content = f"""
    <h1 class="mb-3">Поездки</h1>
    {stats}
    <ul class="list-group shadow-sm">{items}</ul>
    """
    return HttpResponse(page(
        "Поездки", content, active="trips", breadcrumbs=crumbs
    ))


def trip_detail(request, trip_id: int):
    """Страница /trips/<id>/ — информация о поездке."""
    trips = _load_trips()
    trip = next((t for t in trips if t.id == trip_id), None)

    crumbs = _breadcrumbs([
        ("Главная", "/"),
        ("Поездки", "/trips/"),
        (f"Поездка №{trip_id}", None),
    ])

    if trip is None:
        content = """
        <div class="alert alert-warning">
            <h1 class="h4 mb-0">Поездка не найдена</h1>
        </div>
        <a href="/trips/" class="btn btn-outline-secondary">
            ← к списку поездок
        </a>
        """
        return HttpResponse(
            page("Поездка не найдена", content,
                 active="trips", breadcrumbs=crumbs),
            status=404,
        )

    state = "отменена" if trip.is_cancelled else "активна"
    badge = "bg-secondary" if trip.is_cancelled else "bg-success"
    price = trip.calculate_price()

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <h5 class="card-title mb-3">Поездка №{trip.id}</h5>
                <span class="badge {badge} fs-6">{state}</span>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <p>
                        <strong>Маршрут:</strong>
                        <a href="/routes/{trip.route.id}/">
                            {trip.route.number}
                        </a>
                        ({trip.route.transport_type})
                    </p>
                    <p><strong>Пассажир:</strong> {trip.user.name}</p>
                    <p>
                        <strong>Льготы:</strong>
                        {'есть' if trip.user.has_benefits else 'нет'}
                    </p>
                </div>
                <div class="col-md-6">
                    <p>
                        <strong>Откуда:</strong>
                        {trip.stop_from.name}
                    </p>
                    <p>
                        <strong>Куда:</strong>
                        {trip.stop_to.name}
                    </p>
                    <p><strong>Дата:</strong> {trip.date}</p>
                    <p>
                        <strong>Стоимость:</strong>
                        {price:.2f} руб.
                    </p>
                </div>
            </div>
            <a href="/trips/" class="btn btn-outline-secondary">
                ← к списку поездок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(
        f"Поездка №{trip.id}", content,
        active="trips", breadcrumbs=crumbs,
    ))