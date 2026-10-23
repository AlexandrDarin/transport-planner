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
    has_benefits INTEGER NOT NULL DEFAULT 0 CHECK (has_benefits IN (0, 1))
);
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    route_id INTEGER NOT NULL REFERENCES routes(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    stop_from_id INTEGER NOT NULL REFERENCES stops(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    stop_to_id INTEGER NOT NULL REFERENCES stops(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    trip_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0 CHECK (is_cancelled IN (0, 1))
);
CREATE INDEX IF NOT EXISTS idx_trips_route ON trips(route_id);
CREATE INDEX IF NOT EXISTS idx_trips_user ON trips(user_id);
CREATE INDEX IF NOT EXISTS idx_trips_date ON trips(trip_date);
