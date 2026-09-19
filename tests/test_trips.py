from datetime import date

from trips import (
    is_route_free, create_trip, cancel_trip, find_trips_by_user,
)


def test_is_route_free():
    trips = []
    assert is_route_free(trips, 1, date(2026, 9, 15)) is True


def test_create_trip():
    trips = []
    trip = create_trip(trips, 1, date(2026, 9, 15), "Иван")
    assert trip is not None
    assert len(trips) == 1


def test_duplicate_trip_forbidden():
    trips = []
    create_trip(trips, 1, date(2026, 9, 15), "Иван")
    trip2 = create_trip(trips, 1, date(2026, 9, 15), "Пётр")
    assert trip2 is None
    assert len(trips) == 1


def test_cancel_trip():
    trips = []
    create_trip(trips, 1, date(2026, 9, 15), "Иван")
    assert cancel_trip(trips, 1) is True
    assert len(trips) == 0


def test_find_trips_by_user():
    trips = []
    create_trip(trips, 1, date(2026, 9, 15), "Иван")
    create_trip(trips, 2, date(2026, 9, 16), "Пётр")
    assert len(find_trips_by_user(trips, "иван")) == 1