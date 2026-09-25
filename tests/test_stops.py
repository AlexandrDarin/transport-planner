from models import Stop
from models.stops import (
    add_stop, find_stop_by_id, find_stops_by_name,
    filter_stops_by_city, sort_stops_by_name,
)


def test_stop_creation():
    stop = Stop(1, "Улица Ленина", "Москва")
    assert stop.id == 1
    assert stop.name == "Улица Ленина"
    assert stop.city == "Москва"


def test_stop_str():
    stop = Stop(1, "Вокзал", "Москва")
    assert "Вокзал" in str(stop)


def test_stop_from_data():
    stop = Stop.from_data({"id": 1, "name": "Вокзал", "city": "Москва"})
    assert stop.id == 1


def test_add_stop():
    stops = []
    stop = add_stop(stops, "Улица Ленина", "Москва")
    assert stop.id == 1
    assert len(stops) == 1


def test_find_stop_by_id():
    stops = []
    add_stop(stops, "Вокзал", "Москва")
    assert find_stop_by_id(stops, 1).name == "Вокзал"
    assert find_stop_by_id(stops, 99) is None


def test_find_stops_by_name():
    stops = []
    add_stop(stops, "Улица Ленина", "Москва")
    add_stop(stops, "Площадь Победы", "Москва")
    assert len(find_stops_by_name(stops, "площ")) == 1


def test_filter_stops_by_city():
    stops = []
    add_stop(stops, "Вокзал", "Москва")
    add_stop(stops, "Порт", "Сочи")
    assert len(filter_stops_by_city(stops, "Москва")) == 1


def test_sort_stops_by_name():
    stops = []
    add_stop(stops, "Вокзал", "Москва")
    add_stop(stops, "Аэропорт", "Москва")
    ordered = sort_stops_by_name(stops)
    assert ordered[0].name == "Аэропорт"