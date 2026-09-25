"""Класс Trip и функции работы с коллекцией поездок."""

from __future__ import annotations
from datetime import date
from typing import List, Optional

from .routes import Route
from .stops import Stop
from .users import User


class Trip:
    """Поездка пользователя по маршруту."""

    def __init__(self, trip_id: int, route: Route, user: User,
                 stop_from: Stop, stop_to: Stop,
                 trip_date: date) -> None:
        self.id = trip_id
        self.route = route
        self.user = user
        self.stop_from = stop_from
        self.stop_to = stop_to
        self.date = trip_date
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить поездку."""
        self.is_cancelled = True

    def calculate_price(self) -> float:
        """Стоимость поездки с учётом скидки пользователя."""
        return round(self.route.base_price * self.user.get_discount(), 2)

    @classmethod
    def from_data(cls, data: dict, routes: List[Route],
                  users: List[User], stops: List[Stop]) -> Optional["Trip"]:
        """Создать поездку из данных JSON, восстановив связи."""
        route = next((r for r in routes if r.id == data["route_id"]), None)
        user = next((u for u in users if u.id == data["user_id"]), None)
        stop_from = next((s for s in stops
                          if s.id == data["stop_from_id"]), None)
        stop_to = next((s for s in stops
                        if s.id == data["stop_to_id"]), None)
        if not (route and user and stop_from and stop_to):
            return None
        trip = cls(
            trip_id=data["id"],
            route=route,
            user=user,
            stop_from=stop_from,
            stop_to=stop_to,
            trip_date=date.fromisoformat(data["date"]),
        )
        trip.is_cancelled = data.get("is_cancelled", False)
        return trip

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "route_id": self.route.id,
            "user_id": self.user.id,
            "stop_from_id": self.stop_from.id,
            "stop_to_id": self.stop_to.id,
            "date": str(self.date),
            "is_cancelled": self.is_cancelled,
        }

    def __str__(self) -> str:
        status = "отменена" if self.is_cancelled else "активна"
        return (f"#{self.id} | {self.date} | "
                f"{self.route.number} | {self.user.name} | {status}")


# ---------- Функции работы с коллекцией поездок ----------

def is_route_free(trips: List[Trip], route: Route,
                  trip_date: date) -> bool:
    """Свободен ли маршрут на указанную дату."""
    for t in trips:
        if (t.route.id == route.id
                and t.date == trip_date
                and not t.is_cancelled):
            return False
    return True


def create_trip(trips: List[Trip], route: Route, user: User,
                stop_from: Stop, stop_to: Stop,
                trip_date: date) -> Optional[Trip]:
    """Создать поездку, если маршрут свободен на дату."""
    if not is_route_free(trips, route, trip_date):
        return None
    trip_id = max((t.id for t in trips), default=0) + 1
    trip = Trip(trip_id, route, user, stop_from, stop_to, trip_date)
    trips.append(trip)
    return trip


def cancel_trip(trips: List[Trip], trip_id: int) -> bool:
    """Найти поездку по id и отменить её."""
    for t in trips:
        if t.id == trip_id:
            t.cancel()
            return True
    return False


def find_trips_by_user(trips: List[Trip], user: User) -> List[Trip]:
    """Найти все поездки пользователя."""
    return [t for t in trips if t.user.id == user.id]


def get_trip_summary(trip: Trip) -> str:
    """Сводка о поездке."""
    return (
        f"Пассажир: {trip.user.name}\n"
        f"Маршрут: {trip.route.number}\n"
        f"Откуда: {trip.stop_from.name}\n"
        f"Куда: {trip.stop_to.name}\n"
        f"Дата: {trip.date}\n"
        f"Стоимость: {trip.calculate_price():.2f} руб."
    )