"""Импорт исходных JSON-данных ПР3 в SQLite (без удаления JSON)."""
import json
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from db.database import get_connection

DATA_DIR = BASE_DIR / "data"


def read_json(filename, default):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file) if file else default


def import_data():
    routes = read_json("routes.json", {})
    stops = read_json("stops.json", [])
    users = read_json("users.json", [])
    trips = read_json("trips.json", [])
    connection = get_connection()
    try:
        schema = (BASE_DIR / "sql" / "schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.execute("DELETE FROM trips")
        connection.execute("DELETE FROM routes")
        connection.execute("DELETE FROM stops")
        connection.execute("DELETE FROM users")
        connection.executemany(
            "INSERT INTO routes (id, number, transport_type, base_price, travel_time_minutes) VALUES (?, ?, ?, ?, ?)",
            [(int(key), item["number"], item["transport_type"], item["base_price"], item["travel_time_minutes"]) for key, item in routes.items()],
        )
        connection.executemany(
            "INSERT INTO stops (id, name, city) VALUES (?, ?, ?)",
            [(item["id"], item["name"], item["city"]) for item in stops],
        )
        connection.executemany(
            "INSERT INTO users (id, name, age, has_benefits) VALUES (?, ?, ?, ?)",
            [(item["id"], item["name"], item["age"], int(item["has_benefits"])) for item in users],
        )
        connection.executemany(
            "INSERT INTO trips (id, route_id, user_id, stop_from_id, stop_to_id, trip_date, is_cancelled) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(item["id"], item["route_id"], item["user_id"], item["stop_from_id"], item["stop_to_id"], item["date"], int(item.get("is_cancelled", False))) for item in trips],
        )
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    import_data()
    print("JSON-данные импортированы в SQLite.")
