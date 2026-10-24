-- ==========================================
-- Transport Planner: Структура базы данных (ПР7)
-- ==========================================

CREATE TABLE IF NOT EXISTS stops (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    route_number TEXT NOT NULL,
    transport_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    route_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    trip_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (route_id) REFERENCES routes (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
