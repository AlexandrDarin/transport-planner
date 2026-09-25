"""Класс Stop и функции работы с коллекцией остановок."""

from __future__ import annotations
from typing import List


class Stop:
    """Остановка общественного транспорта."""

    def __init__(self, stop_id: int, name: str, city: str) -> None:
        self.id = stop_id
        self.name = name
        self.city = city

    @classmethod
    def from_data(cls, data: dict) -> "Stop":
        """Создать остановку из набора данных."""
        return cls(
            stop_id=data["id"],
            name=data["name"],
            city=data["city"],
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


# ---------- Функции работы с коллекцией остановок ----------

def add_stop(stops: List[Stop], name: str, city: str) -> Stop:
    """Создать остановку и добавить в коллекцию."""
    stop_id = max((s.id for s in stops), default=0) + 1
    stop = Stop(stop_id, name, city)
    stops.append(stop)
    return stop


def find_stop_by_id(stops: List[Stop], stop_id: int) -> Stop | None:
    """Найти остановку по id."""
    for s in stops:
        if s.id == stop_id:
            return s
    return None


def find_stops_by_name(stops: List[Stop], query: str) -> List[Stop]:
    """Найти остановки по подстроке в названии."""
    q = query.lower()
    return [s for s in stops if q in s.name.lower()]


def filter_stops_by_city(stops: List[Stop], city: str) -> List[Stop]:
    """Отобрать остановки по городу."""
    return [s for s in stops if s.city.lower() == city.lower()]


def sort_stops_by_name(stops: List[Stop]) -> List[Stop]:
    """Отсортировать остановки по названию."""
    return sorted(stops, key=lambda s: s.name)