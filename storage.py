"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os
from typing import List

from models import User, Route, Stop, Trip
from models.users import User as _User
from models.routes import Route as _Route
from models.stops import Stop as _Stop
from models.trips import Trip as _Trip


def _read_json(filename: str, default):
    """Прочитать JSON, обработать ошибки."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден — стартуем с пустым значением.")
        return default
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён — стартуем с пустым значением.")
        return default


def _write_json(filename: str, data) -> None:
    """Записать JSON, создав папку при необходимости."""
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей как объекты User."""
    data = _read_json(filename, [])
    return [User.from_data(item) for item in data]


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить пользователей в JSON."""
    _write_json(filename, [u.to_dict() for u in users])


def load_routes(filename: str) -> List[Route]:
    """Загрузить маршруты как объекты Route."""
    data = _read_json(filename, {})
    return [Route.from_data(int(rid), item) for rid, item in data.items()]


def save_routes(filename: str, routes: List[Route]) -> None:
    """Сохранить маршруты в JSON (как словарь по id)."""
    _write_json(filename, {str(r.id): r.to_dict() for r in routes})


def load_stops(filename: str) -> List[Stop]:
    """Загрузить остановки как объекты Stop."""
    data = _read_json(filename, [])
    return [Stop.from_data(item) for item in data]


def save_stops(filename: str, stops: List[Stop]) -> None:
    """Сохранить остановки в JSON."""
    _write_json(filename, [s.to_dict() for s in stops])


def load_trips(filename: str, routes: List[Route],
               users: List[User], stops: List[Stop]) -> List[Trip]:
    """Загрузить поездки как объекты Trip со связями."""
    data = _read_json(filename, [])
    trips = []
    for item in data:
        trip = Trip.from_data(item, routes, users, stops)
        if trip is not None:
            trips.append(trip)
    return trips


def save_trips(filename: str, trips: List[Trip]) -> None:
    """Сохранить поездки в JSON."""
    _write_json(filename, [t.to_dict() for t in trips])