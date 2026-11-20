"""Тесты слоя SQLite (ПР7): схема, импорт из JSON и файл запросов."""

import re
import sqlite3

import pytest

from db import database, import_json
from db.database import BASE_DIR

QUERIES_FILE = BASE_DIR / "sql" / "queries.sql"


@pytest.fixture
def conn(tmp_path, monkeypatch):
    """Временная база, заполненная из JSON."""
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.sqlite3")
    import_json.main()
    connection = database.get_connection()
    yield connection
    connection.close()


def count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


@pytest.mark.smoke
def test_tables_created(conn):
    names = {
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {"routes", "stops", "users", "trips"} <= names


def test_foreign_keys_declared(conn):
    keys = conn.execute("PRAGMA foreign_key_list(trips)").fetchall()
    assert {row["table"] for row in keys} == {"routes", "users", "stops"}


@pytest.mark.smoke
def test_import_counts_match_json(conn):
    assert count(conn, "routes") == len(import_json.load_json(
        import_json.ROUTES_FILE))
    assert count(conn, "stops") == len(import_json.load_json(
        import_json.STOPS_FILE))
    assert count(conn, "users") == len(import_json.load_json(
        import_json.USERS_FILE))
    assert count(conn, "trips") == len(import_json.load_json(
        import_json.TRIPS_FILE))


def test_import_is_repeatable(conn):
    conn.close()
    import_json.main()
    again = database.get_connection()
    try:
        assert count(again, "routes") == 3
    finally:
        again.close()


def test_row_factory_gives_named_access(conn):
    row = conn.execute("SELECT id, number FROM routes WHERE id = 1")
    assert row.fetchone()["number"] == "А-42"


def test_foreign_key_violation_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO trips (id, route_id, user_id, stop_from_id,"
            " stop_to_id, trip_date) VALUES (99, 999, 1, 1, 2, '2026-01-01')"
        )


def test_check_constraint_rejects_negative_price(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO routes VALUES (99, 'X-1', 'Автобус', -5, 10)"
        )


def _statements():
    text = QUERIES_FILE.read_text(encoding="utf-8")
    result = []
    for chunk in text.split(";"):
        lines = [
            line for line in chunk.splitlines()
            if line.strip() and not line.strip().startswith("--")
        ]
        if lines:
            result.append("\n".join(lines))
    return result


def test_queries_file_has_at_least_ten_queries():
    assert len(_statements()) >= 10


@pytest.mark.parametrize("keyword,minimum", [
    ("WHERE", 2), ("JOIN", 2), ("COUNT(", 2), ("GROUP BY", 2),
    ("HAVING", 1), ("ORDER BY", 2), ("LIMIT", 1),
])
def test_queries_cover_required_kinds(keyword, minimum):
    found = sum(1 for sql in _statements() if keyword in sql.upper())
    assert found >= minimum


def test_every_query_executes(conn):
    """Каждый запрос из sql/queries.sql выполняется на реальных данных."""
    for sql in _statements():
        params = [
            "%1%" if "LIKE" in sql else 1
            for _ in range(sql.count("?"))
        ]
        if "trip_date = ?" in sql:
            params = ["2026-09-15"]
        conn.execute(sql, params).fetchall()


def test_free_routes_query(conn):
    sql = next(s for s in _statements() if "NOT IN" in s)
    free = conn.execute(sql, ["2026-09-15"]).fetchall()
    assert [r["number"] for r in free] == ["М-7", "Т-3"]


def test_left_join_keeps_routes_without_trips(conn):
    sql = next(
        s for s in _statements()
        if "LEFT JOIN trips t" in s and "ORDER BY trip_count" in s
        and "HAVING" not in s
    )
    rows = {r["number"]: r["trip_count"] for r in conn.execute(sql)}
    assert rows == {"А-42": 1, "М-7": 0, "Т-3": 0}


def test_having_filters_groups(conn):
    sql = next(s for s in _statements() if "HAVING" in s)
    assert len(conn.execute(sql, [1]).fetchall()) == 1
    assert conn.execute(sql, [2]).fetchall() == []


def test_benefit_price_is_half(conn):
    sql = next(s for s in _statements() if "WHERE t.id = ?" in s)
    trip = conn.execute(sql, [2]).fetchone()
    assert trip["price"] == pytest.approx(20.0)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", trip["trip_date"])
