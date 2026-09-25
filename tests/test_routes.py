from models import Route
from models.routes import (
    add_route, find_routes, filter_routes_by_price,
    sort_routes, route_statistics,
)


def test_route_creation():
    route = Route(1, "А-42", "Автобус", 50.0, 35)
    assert route.id == 1
    assert route.number == "А-42"
    assert route.base_price == 50.0


def test_route_methods():
    route = Route(1, "А-42", "Автобус", 50.0, 35)
    assert route.calculate_travel_time(8) == 43
    assert route.calculate_price(False) == 50.0
    assert route.calculate_price(True) == 25.0


def test_route_str():
    route = Route(1, "А-42", "Автобус", 50.0, 35)
    assert "А-42" in str(route)


def test_route_from_data():
    route = Route.from_data(1, {
        "number": "А-42",
        "transport_type": "Автобус",
        "base_price": 50.0,
        "travel_time_minutes": 35,
    })
    assert route.id == 1
    assert route.number == "А-42"


def test_add_route():
    routes = []
    route = add_route(routes, "А-42", "Автобус", 50.0, 35)
    assert route.id == 1
    assert len(routes) == 1


def test_find_routes():
    routes = []
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    assert len(find_routes(routes, "авто")) == 1


def test_filter_routes_by_price():
    routes = []
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    assert len(filter_routes_by_price(routes, 45.0)) == 1


def test_sort_routes():
    routes = []
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    ordered = sort_routes(routes)
    assert ordered[0].base_price == 40.0


def test_route_statistics():
    routes = []
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    stats = route_statistics(routes)
    assert stats["count"] == 2
    assert stats["avg_price"] == 45.0