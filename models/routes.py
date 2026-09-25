"""Класс Route и функции работы с коллекцией маршрутов."""

from __future__ import annotations
from typing import List


class Route:
    """Маршрут общественного транспорта."""

    def __init__(self, route_id: int, number: str, transport_type: str,
                 base_price: float, travel_time_minutes: int) -> None:
        self.id = route_id
        self.number = number
        self.transport_type = transport_type
        self.base_price = base_price
        self.travel_time_minutes = travel_time_minutes

    def calculate_travel_time(self, stops_count: int) -> int:
        """Время поездки с учётом остановок."""
        return self.travel_time_minutes + stops_count

    def calculate_price(self, has_benefits: bool) -> float:
        """Стоимость проезда с учётом льгот."""
        if has_benefits:
            return self.base_price * 0.5
        return self.base_price

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверить корректность цены."""
        return price >= 0

    @classmethod
    def from_data(cls, route_id: int, data: dict) -> "Route":
        """Создать маршрут из набора данных."""
        return cls(
            route_id=route_id,
            number=data["number"],
            transport_type=data["transport_type"],
            base_price=data["base_price"],
            travel_time_minutes=data["travel_time_minutes"],
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "number": self.number,
            "transport_type": self.transport_type,
            "base_price": self.base_price,
            "travel_time_minutes": self.travel_time_minutes,
        }

    def __str__(self) -> str:
        return (f"{self.number} ({self.transport_type}), "
                f"{self.base_price} руб., {self.travel_time_minutes} мин.")


# ---------- Функции работы с коллекцией маршрутов ----------

def add_route(routes: List[Route], number: str, transport_type: str,
              base_price: float, travel_time_minutes: int) -> Route:
    """Создать маршрут и добавить в коллекцию."""
    route_id = max((r.id for r in routes), default=0) + 1
    route = Route(route_id, number, transport_type,
                  base_price, travel_time_minutes)
    routes.append(route)
    return route


def find_routes(routes: List[Route], query: str) -> List[Route]:
    """Найти маршруты по подстроке в номере или виде транспорта."""
    q = query.lower()
    return [r for r in routes
            if q in r.number.lower() or q in r.transport_type.lower()]


def filter_routes_by_price(routes: List[Route],
                           max_price: float) -> List[Route]:
    """Отобрать маршруты с ценой не выше max_price."""
    return [r for r in routes if r.base_price <= max_price]


def sort_routes(routes: List[Route]) -> List[Route]:
    """Отсортировать маршруты по цене (lambda)."""
    return sorted(routes, key=lambda r: r.base_price)


def route_statistics(routes: List[Route]) -> dict:
    """Статистика по маршрутам."""
    if not routes:
        return {"count": 0, "min_price": 0, "max_price": 0, "avg_price": 0}
    prices = [r.base_price for r in routes]
    return {
        "count": len(routes),
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": round(sum(prices) / len(prices), 2),
    }


# ---------- Совместимость с тестами ПР1/ПР2 ----------

def is_route_available(route_number: str, stop_from: str,
                       stop_to: str) -> bool:
    """Проверка доступности маршрута (функция из ПР1)."""
    return bool(route_number and stop_from and stop_to)


def calculate_travel_time(travel_time_minutes: int,
                          stops_count: int) -> int:
    """Совместимость с тестом ПР1."""
    return travel_time_minutes + stops_count


def calculate_price(base_price: float, has_benefits: bool) -> float:
    """Совместимость с тестом ПР1."""
    return base_price * 0.5 if has_benefits else base_price


def get_route_status(is_available: bool) -> str:
    """Текстовый статус маршрута."""
    if is_available:
        return "Маршрут доступен для поездки"
    return "Маршрут недоступен"