"""Тесты веб-интерфейса: шаблоны Django (ПР6) и данные из SQLite (ПР7)."""

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transport_planner.settings")
django.setup()

from django.template.loader import get_template  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

from db import database, import_json  # noqa: E402
from homepage import views as homepage_views  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "web.sqlite3")
    import_json.main()
    return Client()


PAGES = [
    "homepage:index", "homepage:about", "homepage:statistics",
    "routes:list", "routes:available", "stops:list", "trips:list",
    "users:list",
]


@pytest.mark.smoke
@pytest.mark.parametrize("name", PAGES)
def test_pages_open(client, name):
    assert client.get(reverse(name)).status_code == 200


@pytest.mark.parametrize("name,pk", [
    ("routes:detail", 1), ("stops:detail", 1),
    ("trips:detail", 1), ("users:detail", 1),
])
def test_detail_pages_open(client, name, pk):
    assert client.get(reverse(name, args=[pk])).status_code == 200


@pytest.mark.parametrize("name", [
    "routes:detail", "stops:detail", "trips:detail", "users:detail",
])
def test_missing_object_returns_404_page(client, name):
    response = client.get(reverse(name, args=[9999]))
    assert response.status_code == 404
    assert "не найден" in response.content.decode()


def test_non_int_id_is_not_routed(client):
    assert client.get("/routes/abc/").status_code == 404


def test_routes_come_from_database(client):
    html = client.get(reverse("routes:list")).content.decode()
    assert "А-42" in html and "Т-3" in html


def test_routes_search_is_parametrized(client):
    url = reverse("routes:list")
    html = client.get(url, {"q": "Трамвай"}).content.decode()
    assert "Т-3" in html and "А-42" not in html
    # SQL-инъекция воспринимается как обычный текст
    injection = client.get(url, {"q": "' OR 1=1 --"})
    assert injection.status_code == 200
    assert "А-42" not in injection.content.decode()


def test_routes_price_filter(client):
    html = client.get(
        reverse("routes:list"), {"max_price": "45"}
    ).content.decode()
    assert "Т-3" in html and "А-42" not in html


def test_empty_result_message(client):
    html = client.get(reverse("routes:list"), {"q": "нет-такого"})
    assert "Маршруты не найдены." in html.content.decode()


def test_available_routes_by_date(client):
    url = reverse("routes:available")
    busy = client.get(url, {"date": "2026-09-15"}).content.decode()
    assert "М-7" in busy and "А-42" not in busy
    free = client.get(url, {"date": "2030-01-01"}).content.decode()
    assert "А-42" in free


def test_trips_status_filter(client):
    url = reverse("trips:list")
    active = client.get(url, {"status": "active"}).content.decode()
    cancelled = client.get(url, {"status": "cancelled"}).content.decode()
    assert "Активна" in active and "Отменена" not in active
    assert "Отменена" in cancelled and "Активна" not in cancelled


def test_trip_detail_shows_discount_price(client):
    html = client.get(reverse("trips:detail", args=[2])).content.decode()
    assert "20,00" in html or "20.00" in html
    assert "скидка 50%" in html


def test_statistics_having_threshold(client):
    url = reverse("homepage:statistics")
    one = client.get(url, {"min_trips": "1"}).content.decode()
    two = client.get(url, {"min_trips": "2"}).content.decode()
    assert "Маршрутов с таким количеством поездок нет." not in one
    assert "Маршрутов с таким количеством поездок нет." in two


def test_navigation_uses_named_urls_and_static(client):
    html = client.get(reverse("homepage:index")).content.decode()
    for name in ("routes:list", "stops:list", "trips:list",
                 "users:list", "homepage:statistics"):
        assert f'href="{reverse(name)}"' in html
    assert "homepage/css/style.css" in html
    assert "homepage/img/logo.png" in html
    assert "homepage/js/main.js" in html


def test_template_inheritance_and_includes():
    assert get_template("routes_app/list.html")
    assert get_template("includes/navigation.html")
    assert get_template("trips_app/includes/trip_status.html")
    assert get_template("routes_app/includes/route_card.html")


def test_page_function_is_gone():
    assert not hasattr(homepage_views, "page")
