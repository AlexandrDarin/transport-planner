import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def test_database_has_expected_tables_and_rows():
    connection = sqlite3.connect(BASE_DIR / "data" / "transport_planner.sqlite3")
    try:
        tables = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert {"stops", "routes", "users", "trips"} <= tables
        assert connection.execute("SELECT COUNT(*) FROM stops").fetchone()[0] == len(
            json.loads((BASE_DIR / "data" / "stops.json").read_text(encoding="utf-8"))
        )
        assert connection.execute("SELECT COUNT(*) FROM routes").fetchone()[0] == len(
            json.loads((BASE_DIR / "data" / "routes.json").read_text(encoding="utf-8"))
        )
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == len(
            json.loads((BASE_DIR / "data" / "users.json").read_text(encoding="utf-8"))
        )
        assert connection.execute("SELECT COUNT(*) FROM trips").fetchone()[0] == len(
            json.loads((BASE_DIR / "data" / "trips.json").read_text(encoding="utf-8"))
        )
    finally:
        connection.close()


def test_foreign_keys_are_valid():
    connection = sqlite3.connect(BASE_DIR / "data" / "transport_planner.sqlite3")
    try:
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        connection.close()


def test_parameterized_availability_query():
    connection = sqlite3.connect(BASE_DIR / "data" / "transport_planner.sqlite3")
    try:
        rows = connection.execute(
            "SELECT id FROM routes WHERE id NOT IN "
            "(SELECT route_id FROM trips WHERE trip_date = ? AND is_cancelled = 0)",
            ("2026-10-25",),
        ).fetchall()
        assert [row[0] for row in rows] == [2]
    finally:
        connection.close()
