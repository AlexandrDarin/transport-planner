import json
import os

from db.database import get_connection

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def main():
    stops = load_json("stops.json")
    routes = load_json("routes.json")
    users = load_json("users.json")
    trips = load_json("trips.json")
    conn = get_connection()
    try:
        conn.execute("DELETE FROM trips")
        conn.execute("DELETE FROM routes")
        conn.execute("DELETE FROM stops")
        conn.execute("DELETE FROM users")
        conn.executemany(
            "INSERT INTO stops (id, name, latitude, longitude) VALUES (?, ?, ?, ?)",
            [(s["id"], s["name"], s["latitude"], s["longitude"]) for s in stops],
        )
        conn.executemany(
            "INSERT INTO routes (id, title, route_number, transport_type) VALUES (?, ?, ?, ?)",
            [(r["id"], r["title"], r["route_number"], r["transport_type"]) for r in routes],
        )
        conn.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            [(u["id"], u["name"], u["email"]) for u in users],
        )
        conn.executemany(
            "INSERT INTO trips (id, route_id, user_id, trip_date, is_cancelled) VALUES (?, ?, ?, ?, ?)",
            [(t["id"], t["route_id"], t["user_id"], t["trip_date"], int(t["is_cancelled"])) for t in trips],
        )
        conn.commit()
        print("Импорт данных из JSON в SQLite выполнен успешно.")
        for table in ("stops", "routes", "users", "trips"):
            count = conn.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
            print(f"{table}: {count}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
