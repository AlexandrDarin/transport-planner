"""Подключение Python к SQLite для индивидуального проекта."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "transport_planner.sqlite3"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection():
    """Вернуть соединение с БД.

    * PRAGMA foreign_keys = ON включает проверку внешних ключей
      (по умолчанию SQLite её не выполняет);
    * row_factory = sqlite3.Row позволяет обращаться к полям строки
      по имени: row["number"] и {{ route.number }} в шаблоне.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn):
    """Создать таблицы из sql/schema.sql (безопасно при повторе)."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
