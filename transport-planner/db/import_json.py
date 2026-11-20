"""Однократный перенос данных из JSON-файлов в SQLite.

Запуск из корня проекта:  python -m db.import_json
JSON-файлы не удаляются: они нужны консольной версии (main.py).
"""

import json

from db.database import BASE_DIR, create_schema, get_connection

DATA_DIR = BASE_DIR / "data"
ROUTES_FILE = DATA_DIR / "routes.json"
STOPS_FILE = DATA_DIR / "stops.json"
USERS_FILE = DATA_DIR / "users.json"
TRIPS_FILE = DATA_DIR / "trips.json"


def load_json(filename):
    """Прочитать JSON-файл."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_routes(conn):
    """routes.json хранится словарём {id: данные}."""
    routes = load_json(ROUTES_FILE)
    conn.executemany(
        """
        INSERT INTO routes (
            id, number, transport_type, base_price, travel_time_minutes
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                int(route_id),
                route["number"],
                route["transport_type"],
                route["base_price"],
                route["travel_time_minutes"],
            )
            for route_id, route in routes.items()
        ],
    )


def import_stops(conn):
    """Остановки."""
    stops = load_json(STOPS_FILE)
    conn.executemany(
        "INSERT INTO stops (id, name, city) VALUES (?, ?, ?)",
        [(s["id"], s["name"], s["city"]) for s in stops],
    )


def import_users(conn):
    """Пользователи; логическое значение приводится к 0/1."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, age, has_benefits)
        VALUES (?, ?, ?, ?)
        """,
        [
            (u["id"], u["name"], u["age"], int(u["has_benefits"]))
            for u in users
        ],
    )


def import_trips(conn):
    """Поездки импортируются последними: они ссылаются на остальные."""
    trips = load_json(TRIPS_FILE)
    conn.executemany(
        """
        INSERT INTO trips (
            id, route_id, user_id, stop_from_id, stop_to_id,
            trip_date, is_cancelled
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                t["id"],
                t["route_id"],
                t["user_id"],
                t["stop_from_id"],
                t["stop_to_id"],
                t["date"],
                int(t.get("is_cancelled", False)),
            )
            for t in trips
        ],
    )


def main():
    """Создать таблицы, очистить их и перенести данные одной транзакцией."""
    conn = get_connection()
    try:
        create_schema(conn)
        for table in ("trips", "routes", "stops", "users"):
            conn.execute(f"DELETE FROM {table}")  # имена таблиц — константы
        import_routes(conn)
        import_stops(conn)
        import_users(conn)
        import_trips(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("JSON-данные импортированы в SQLite.")


if __name__ == "__main__":
    main()
