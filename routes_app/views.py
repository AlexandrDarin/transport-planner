"""View-функции приложения routes_app."""

from datetime import date

from django.http import HttpResponse

from homepage.views import page, _breadcrumbs
from models.trips import is_route_free
from storage import load_routes, load_trips, load_users, load_stops


def routes_list(request):
    """Страница /routes/ — список маршрутов с поиском."""
    routes = load_routes("data/routes.json")
    query = request.GET.get("q", "").strip()
    if query:
        q = query.lower()
        routes = [r for r in routes
                  if q in r.number.lower()
                  or q in r.transport_type.lower()]

    stats = ""
    if routes:
        prices = [r.base_price for r in routes]
        stats = f"""
        <div class="row g-3 mb-3">
            <div class="col-md-4">
                <div class="stat-card">
                    <div class="stat-value">{len(routes)}</div>
                    <div class="stat-label">маршрутов</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card">
                    <div class="stat-value">{min(prices)}</div>
                    <div class="stat-label">мин. цена, руб.</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card">
                    <div class="stat-value">{max(prices)}</div>
                    <div class="stat-label">макс. цена, руб.</div>
                </div>
            </div>
        </div>
        """

    items = ""
    for r in routes:
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<div>'
            f'<a href="/routes/{r.id}/" class="fw-bold text-decoration-none">'
            f'{r.number}</a> '
            f'<span class="text-muted">({r.transport_type})</span>'
            f'</div>'
            f'<div>'
            f'<span class="badge badge-time me-2">'
            f'{r.travel_time_minutes} мин.</span>'
            f'<span class="badge badge-price">'
            f'{r.base_price} руб.</span>'
            f'</div></li>'
        )

    if not items:
        items = (
            '<li class="list-group-item text-muted">'
            'Маршруты не найдены.</li>'
        )

    search = f"""
    <form method="get" class="mb-3">
        <div class="input-group">
            <input type="text" name="q" class="form-control"
                   placeholder="Поиск по номеру или транспорту"
                   value="{query}">
            <button class="btn btn-primary" type="submit">
                Найти
            </button>
        </div>
    </form>
    """

    content = f"""
    <h1 class="mb-3">Маршруты</h1>
    {search}
    {stats}
    <ul class="list-group shadow-sm">{items}</ul>
    """
    crumbs = _breadcrumbs([("Главная", "/"), ("Маршруты", None)])
    return HttpResponse(page(
        "Маршруты", content, active="routes", breadcrumbs=crumbs
    ))


def route_detail(request, route_id: int):
    """Страница /routes/<id>/ — информация о маршруте."""
    routes = load_routes("data/routes.json")
    route = next((r for r in routes if r.id == route_id), None)

    crumbs = _breadcrumbs([
        ("Главная", "/"),
        ("Маршруты", "/routes/"),
        (f"Маршрут {route_id}", None),
    ])

    if route is None:
        content = """
        <div class="alert alert-warning">
            <h1 class="h4 mb-0">Маршрут не найден</h1>
        </div>
        <a href="/routes/" class="btn btn-outline-secondary">
            ← к списку маршрутов
        </a>
        """
        return HttpResponse(
            page("Маршрут не найден", content,
                 active="routes", breadcrumbs=crumbs),
            status=404,
        )

    users = load_users("data/users.json")
    stops = load_stops("data/stops.json")
    trips = load_trips("data/trips.json", routes, users, stops)
    trips_of_route = [t for t in trips if t.route.id == route_id]
    free_today = is_route_free(trips, route, date.today())

    status_badge = (
        '<span class="badge bg-success">доступен сегодня</span>'
        if free_today
        else '<span class="badge bg-danger">занят сегодня</span>'
    )

    trips_html = ""
    if trips_of_route:
        for t in trips_of_route:
            state = "отменена" if t.is_cancelled else "активна"
            badge = "bg-secondary" if t.is_cancelled else "bg-success"
            trips_html += (
                f'<li class="list-group-item d-flex '
                f'justify-content-between align-items-center">'
                f'<a href="/trips/{t.id}/">Поездка №{t.id} — {t.date}</a>'
                f'<span class="badge {badge}">{state}</span></li>'
            )
    else:
        trips_html = (
            '<li class="list-group-item text-muted">'
            'Поездок по этому маршруту пока нет.</li>'
        )

    content = f"""
    <div class="card shadow-sm mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <h5 class="card-title mb-3">
                    Маршрут {route.number}
                </h5>
                {status_badge}
            </div>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>ID:</strong> {route.id}</p>
                    <p><strong>Транспорт:</strong> {route.transport_type}</p>
                    <p><strong>Цена:</strong> {route.base_price} руб.</p>
                </div>
                <div class="col-md-6">
                    <p>
                        <strong>Время в пути:</strong>
                        {route.travel_time_minutes} мин.
                    </p>
                    <p>
                        <strong>Поездок всего:</strong>
                        {len(trips_of_route)}
                    </p>
                </div>
            </div>
            <a href="/routes/" class="btn btn-outline-secondary">
                ← к списку маршрутов
            </a>
        </div>
    </div>

    <h6 class="mb-2">Поездки по маршруту</h6>
    <ul class="list-group shadow-sm">{trips_html}</ul>
    """
    return HttpResponse(page(
        f"Маршрут {route.number}", content,
        active="routes", breadcrumbs=crumbs,
    ))