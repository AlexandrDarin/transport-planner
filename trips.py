"""Функции для работы с поездками."""

from datetime import date


def is_route_free(trips: list[dict], route_id: int,
                  trip_date: date) -> bool:
    """Свободен ли маршрут на указанную дату."""
    for t in trips:
        if t["route_id"] == route_id and t["date"] == str(trip_date):
            return False
    return True


def create_trip(trips: list[dict], route_id: int, trip_date: date,
                user_id: int, stop_from_id: int, stop_to_id: int):
    """Создать поездку, если маршрут свободен на эту дату."""
    if not is_route_free(trips, route_id, trip_date):
        return None
    trip_id = max((t["id"] for t in trips), default=0) + 1
    trip = {
        "id": trip_id,
        "route_id": route_id,
        "user_id": user_id,
        "stop_from_id": stop_from_id,
        "stop_to_id": stop_to_id,
        "date": str(trip_date),
    }
    trips.append(trip)
    return trip


def cancel_trip(trips: list[dict], trip_id: int) -> bool:
    """Отменить поездку по id. True — если удалось."""
    for i, t in enumerate(trips):
        if t["id"] == trip_id:
            trips.pop(i)
            return True
    return False


def find_trips_by_user(trips: list[dict], user_id: int) -> list[dict]:
    """Найти все поездки пользователя по id."""
    return [t for t in trips if t["user_id"] == user_id]


def get_trip_summary(user_name: str, route_number: str, stop_from: str,
                     stop_to: str, travel_time: int, price: float) -> str:
    """Сводка о поездке (функция из ПР1)."""
    return (
        f"Пассажир: {user_name}\n"
        f"Маршрут: {route_number}\n"
        f"Откуда: {stop_from}\n"
        f"Куда: {stop_to}\n"
        f"Время в пути: ~{travel_time} мин.\n"
        f"Стоимость: {price:.2f} руб."
    )