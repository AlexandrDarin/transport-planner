"""Функции для работы с маршрутами."""


def is_route_available(route_number: str, stop_from: str,
                       stop_to: str) -> bool:
    """Проверка доступности маршрута (функция из ПР1)."""
    return bool(route_number and stop_from and stop_to)


def calculate_travel_time(travel_time_minutes: int,
                          stops_count: int) -> int:
    """Расчёт времени поездки (функция из ПР1)."""
    return travel_time_minutes + stops_count


def calculate_price(base_price: float, has_benefits: bool) -> float:
    """Расчёт стоимости проезда (функция из ПР1)."""
    if has_benefits:
        return base_price * 0.5
    return base_price


def get_route_status(is_available: bool) -> str:
    """Текстовый статус маршрута."""
    if is_available:
        return "Маршрут доступен для поездки"
    return "Маршрут недоступен"


def add_route(routes: dict[int, dict], number: str, transport_type: str,
              base_price: float, travel_time_minutes: int) -> int:
    """Добавить маршрут в словарь routes и вернуть его id."""
    route_id = max(routes.keys(), default=0) + 1
    routes[route_id] = {
        "number": number,
        "transport_type": transport_type,
        "base_price": base_price,
        "travel_time_minutes": travel_time_minutes,
    }
    return route_id


def find_routes(routes: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти маршруты по подстроке в номере или виде транспорта."""
    q = query.lower()
    return {
        rid: r for rid, r in routes.items()
        if q in r["number"].lower() or q in r["transport_type"].lower()
    }


def filter_routes_by_price(routes: dict[int, dict],
                           max_price: float) -> dict[int, dict]:
    """Отобрать маршруты с ценой не выше max_price."""
    return {rid: r for rid, r in routes.items()
            if r["base_price"] <= max_price}


def sort_routes(routes: dict[int, dict]) -> list[tuple[int, dict]]:
    """Отсортировать маршруты по цене (lambda-функция)."""
    return sorted(routes.items(), key=lambda item: item[1]["base_price"])


def route_statistics(routes: dict[int, dict]) -> dict:
    """Сводная статистика по маршрутам."""
    if not routes:
        return {"count": 0, "min_price": 0, "max_price": 0, "avg_price": 0}
    prices = [r["base_price"] for r in routes.values()]
    return {
        "count": len(routes),
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": round(sum(prices) / len(prices), 2),
    }