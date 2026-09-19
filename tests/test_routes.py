from routes import (
    add_route, find_routes, filter_routes_by_price,
    sort_routes, route_statistics,
)


def test_add_route():
    routes = {}
    rid = add_route(routes, "А-42", "Автобус", 50.0, 35)
    assert rid == 1
    assert len(routes) == 1


def test_find_routes():
    routes = {}
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    assert len(find_routes(routes, "авто")) == 1


def test_filter_routes_by_price():
    routes = {}
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    result = filter_routes_by_price(routes, 45.0)
    assert len(result) == 1


def test_sort_routes():
    routes = {}
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    ordered = sort_routes(routes)
    assert ordered[0][1]["base_price"] == 40.0


def test_route_statistics_empty():
    assert route_statistics({})["count"] == 0


def test_route_statistics():
    routes = {}
    add_route(routes, "А-42", "Автобус", 50.0, 35)
    add_route(routes, "Т-3", "Трамвай", 40.0, 25)
    stats = route_statistics(routes)
    assert stats["count"] == 2
    assert stats["avg_price"] == 45.0