from datetime import date

from django.shortcuts import render
from db.database import get_connection


def index(request):
    conn = get_connection()
    try:
        counts = {
            "routes_count": conn.execute("SELECT COUNT(*) FROM routes").fetchone()[0],
            "stops_count": conn.execute("SELECT COUNT(*) FROM stops").fetchone()[0],
            "active_trips_count": conn.execute(
                "SELECT COUNT(*) FROM trips WHERE is_cancelled = 0"
            ).fetchone()[0],
        }
    finally:
        conn.close()
    return render(request, "homepage/index.html", counts)


def routes_list(request):
    conn = get_connection()
    try:
        routes = conn.execute(
            "SELECT id, title, route_number, transport_type FROM routes "
            "ORDER BY route_number"
        ).fetchall()
    finally:
        conn.close()
    return render(request, "homepage/routes.html", {"routes": routes})


def stops_list(request):
    conn = get_connection()
    try:
        stops = conn.execute(
            "SELECT id, name, latitude, longitude FROM stops ORDER BY name"
        ).fetchall()
    finally:
        conn.close()
    return render(request, "homepage/stops.html", {"stops": stops})


def trips_list(request):
    conn = get_connection()
    try:
        trips = conn.execute("""
            SELECT trips.id, trips.trip_date, routes.title AS route_title,
                   routes.route_number, users.name AS user_name, users.email
            FROM trips
            JOIN routes ON trips.route_id = routes.id
            JOIN users ON trips.user_id = users.id
            WHERE trips.is_cancelled = 0
            ORDER BY trips.trip_date;
        """).fetchall()
    finally:
        conn.close()
    return render(request, "homepage/trips.html", {"trips": trips})


def available_routes(request):
    trip_date = request.GET.get("date", "").strip()
    routes = []
    error = ""
    if trip_date:
        try:
            date.fromisoformat(trip_date)
        except ValueError:
            error = "Введите дату в формате ГГГГ-ММ-ДД."
        else:
            conn = get_connection()
            try:
                routes = conn.execute("""
                    SELECT id, title, route_number, transport_type
                    FROM routes
                    WHERE id NOT IN (
                        SELECT route_id FROM trips
                        WHERE trip_date = ? AND is_cancelled = 0
                    )
                    ORDER BY route_number;
                """, (trip_date,)).fetchall()
            finally:
                conn.close()
    return render(request, "homepage/available_routes.html", {
        "routes": routes,
        "trip_date": trip_date,
        "error": error,
        "searched": bool(trip_date) and not error,
    })


def statistics(request):
    conn = get_connection()
    try:
        stats = conn.execute("""
            SELECT routes.title AS route_title, routes.route_number,
                   COUNT(trips.id) AS trips_count
            FROM routes
            LEFT JOIN trips
              ON routes.id = trips.route_id AND trips.is_cancelled = 0
            GROUP BY routes.id, routes.title, routes.route_number
            ORDER BY trips_count DESC, routes.route_number;
        """).fetchall()
        active_trips_count = conn.execute(
            "SELECT COUNT(*) FROM trips WHERE is_cancelled = 0"
        ).fetchone()[0]
    finally:
        conn.close()
    return render(request, "homepage/statistics.html", {
        "statistics": stats,
        "active_trips_count": active_trips_count,
    })
