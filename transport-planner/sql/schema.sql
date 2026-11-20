-- ==========================================================
-- Transport Planner: структура базы данных SQLite
-- ==========================================================
-- Булевы значения хранятся как INTEGER: 0 — нет, 1 — да.
-- Дата поездки хранится строкой YYYY-MM-DD (сравнима и сортируема).
-- Все поля обязательны (NOT NULL): в исходных JSON они всегда заданы.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL,
    transport_type TEXT NOT NULL,
    base_price REAL NOT NULL CHECK (base_price >= 0),
    travel_time_minutes INTEGER NOT NULL CHECK (travel_time_minutes >= 0)
);

CREATE TABLE IF NOT EXISTS stops (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0),
    has_benefits INTEGER NOT NULL DEFAULT 0
        CHECK (has_benefits IN (0, 1))
);

CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    route_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    stop_from_id INTEGER NOT NULL,
    stop_to_id INTEGER NOT NULL,
    trip_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0
        CHECK (is_cancelled IN (0, 1)),
    FOREIGN KEY (route_id) REFERENCES routes(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stop_from_id) REFERENCES stops(id),
    FOREIGN KEY (stop_to_id) REFERENCES stops(id)
);

CREATE INDEX IF NOT EXISTS idx_trips_route ON trips(route_id);
CREATE INDEX IF NOT EXISTS idx_trips_user ON trips(user_id);
CREATE INDEX IF NOT EXISTS idx_trips_date ON trips(trip_date);
