"""View-функции приложения stops_app."""

from django.http import HttpResponse

from homepage.views import page, _breadcrumbs
from storage import (
    load_routes, load_users, load_stops, load_trips,
)


def stops_list(request):
    """Страница /stops/ — список остановок."""
    stops = load_stops("data/stops.json")
    crumbs = _breadcrumbs([("Главная", "/"), ("Остановки", None)])

    if not stops:
        content = """
        <h1 class="mb-3">Остановки</h1>
        <div class="alert alert-info">Остановок пока нет.</div>
        """
        return HttpResponse(page(
            "Остановки", content, active="stops", breadcrumbs=crumbs
        ))

    cities = {s.city for s in stops}

    stats = f"""
    <div class="row g-3 mb-3">
        <div class="col-md-6">
            <div class="stat-card">
                <div class="stat-value">{len(stops)}</div>
                <div class="stat-label">остановок</div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="stat-card">
                <div class="stat-value">{len(cities)}</div>
                <div class="stat-label">городов</div>
            </div>
        </div>
    </div>
    """

    items = ""
    for s in stops:
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<div>'
            f'<a href="/stops/{s.id}/" '
            f'class="fw-bold text-decoration-none">{s.name}</a>'
            f'</div>'
            f'<span class="badge bg-info text-dark">{s.city}</span>'
            f'</li>'
        )

    content = f"""
    <h1 class="mb-3">Остановки</h1>
    {stats}
    <ul class="list-group shadow-sm">{items}</ul>
    """
    return HttpResponse(page(
        "Остановки", content, active="stops", breadcrumbs=crumbs
    ))


def stop_detail(request, stop_id: int):
    """Страница /stops/<id>/ — информация об остановке."""
    stops = load_stops("data/stops.json")
    stop = next((s for s in stops if s.id == stop_id), None)

    crumbs = _breadcrumbs([
        ("Главная", "/"),
        ("Остановки", "/stops/"),
        (f"Остановка {stop_id}", None),
    ])

    if stop is None:
        content = """
        <div class="alert alert-warning">
            <h1 class="h4 mb-0">Остановка не найдена</h1>
        </div>
        <a href="/stops/" class="btn btn-outline-secondary">
            ← к списку остановок
        </a>
        """
        return HttpResponse(
            page("Остановка не найдена", content,
                 active="stops", breadcrumbs=crumbs),
            status=404,
        )

    routes = load_routes("data/routes.json")
    users = load_users("data/users.json")
    trips = load_trips("data/trips.json", routes, users, stops)

    trips_from = [t for t in trips if t.stop_from.id == stop_id]
    trips_to = [t for t in trips if t.stop_to.id == stop_id]

    def render_trips(items):
        if not items:
            return (
                '<li class="list-group-item text-muted">'
                'Поездок нет.</li>'
            )
        html = ""
        for t in items:
            state = "отменена" if t.is_cancelled else "активна"
            badge = "bg-secondary" if t.is_cancelled else "bg-success"
            html += (
                f'<li class="list-group-item d-flex '
                f'justify-content-between align-items-center">'
                f'<a href="/trips/{t.id}/">Поездка №{t.id} · '
                f'{t.date}</a>'
                f'<span class="badge {badge}">{state}</span></li>'
            )
        return html

    content = f"""
    <div class="card shadow-sm mb-4">
        <div class="card-body">
            <h5 class="card-title mb-3">{stop.name}</h5>
            <p><strong>ID:</strong> {stop.id}</p>
            <p><strong>Город:</strong> {stop.city}</p>
            <a href="/stops/" class="btn btn-outline-secondary">
                ← к списку остановок
            </a>
        </div>
    </div>

    <div class="row g-3">
        <div class="col-md-6">
            <h6 class="mb-2">Отправление отсюда</h6>
            <ul class="list-group shadow-sm">
                {render_trips(trips_from)}
            </ul>
        </div>
        <div class="col-md-6">
            <h6 class="mb-2">Прибытие сюда</h6>
            <ul class="list-group shadow-sm">
                {render_trips(trips_to)}
            </ul>
        </div>
    </div>
    """
    return HttpResponse(page(
        stop.name, content, active="stops", breadcrumbs=crumbs
    ))