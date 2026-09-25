"""Функции для работы с остановками."""


def add_stop(stops: list[dict], name: str, city: str) -> int:
    """Добавить остановку в список stops и вернуть её id."""
    stop_id = max((s["id"] for s in stops), default=0) + 1
    stops.append({
        "id": stop_id,
        "name": name,
        "city": city,
    })
    return stop_id


def find_stop_by_id(stops: list[dict], stop_id: int) -> dict | None:
    """Найти остановку по id. None — если нет."""
    for s in stops:
        if s["id"] == stop_id:
            return s
    return None


def find_stops_by_name(stops: list[dict], query: str) -> list[dict]:
    """Найти остановки по подстроке в названии."""
    q = query.lower()
    return [s for s in stops if q in s["name"].lower()]


def filter_stops_by_city(stops: list[dict], city: str) -> list[dict]:
    """Отобрать остановки по городу."""
    return [s for s in stops if s["city"].lower() == city.lower()]


def sort_stops_by_name(stops: list[dict]) -> list[dict]:
    """Отсортировать остановки по названию (lambda)."""
    return sorted(stops, key=lambda s: s["name"])