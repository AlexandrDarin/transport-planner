from datetime import date

from models import User, Route, Stop, Trip
from models.trips import (
    is_route_free, create_trip, cancel_trip,
    find_trips_by_user, get_trip_summary,
)


def _make_objects():
    user = User(1, "Иван", 22, False)
    route = Route(1, "А-42", "Автобус", 50.0, 35)
    stop_a = Stop(1, "Улица Ленина", "Москва")
    stop_b = Stop(2, "Площадь Победы", "Москва")
    return user, route, stop_a, stop_b


def test_trip_creation():
    user, route, stop_a, stop_b = _make_objects()
    trip = Trip(1, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert trip.id == 1
    assert trip.route is route
    assert trip.user is user
    assert trip.is_cancelled is False


def test_trip_cancel():
    user, route, stop_a, stop_b = _make_objects()
    trip = Trip(1, route, user, stop_a, stop_b, date(2026, 9, 15))
    trip.cancel()
    assert trip.is_cancelled is True


def test_trip_price_with_benefits():
    user = User(1, "Пётр", 70, True)
    route = Route(1, "А-42", "Автобус", 50.0, 35)
    stop_a = Stop(1, "A", "M")
    stop_b = Stop(2, "B", "M")
    trip = Trip(1, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert trip.calculate_price() == 25.0


def test_trip_str():
    user, route, stop_a, stop_b = _make_objects()
    trip = Trip(1, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert "А-42" in str(trip)


def test_is_route_free():
    user, route, stop_a, stop_b = _make_objects()
    assert is_route_free([], route, date(2026, 9, 15)) is True


def test_create_trip():
    user, route, stop_a, stop_b = _make_objects()
    trips = []
    trip = create_trip(trips, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert trip is not None
    assert len(trips) == 1


def test_duplicate_trip_forbidden():
    user, route, stop_a, stop_b = _make_objects()
    trips = []
    create_trip(trips, route, user, stop_a, stop_b, date(2026, 9, 15))
    trip2 = create_trip(trips, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert trip2 is None


def test_cancel_trip_allows_new():
    user, route, stop_a, stop_b = _make_objects()
    trips = []
    create_trip(trips, route, user, stop_a, stop_b, date(2026, 9, 15))
    cancel_trip(trips, 1)
    trip2 = create_trip(trips, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert trip2 is not None


def test_find_trips_by_user():
    user, route, stop_a, stop_b = _make_objects()
    trips = []
    create_trip(trips, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert len(find_trips_by_user(trips, user)) == 1


def test_get_trip_summary():
    user, route, stop_a, stop_b = _make_objects()
    trip = Trip(1, route, user, stop_a, stop_b, date(2026, 9, 15))
    assert "Иван" in get_trip_summary(trip)