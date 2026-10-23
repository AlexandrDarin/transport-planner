"""Страницы остановок на основе SQLite."""

from django.shortcuts import render

from db.database import get_connection

ALL_STOPS_SQL = """
    SELECT id, name, city
    FROM stops
    ORDER BY city, name;
"""

SEARCH_STOPS_SQL = """
    SELECT id, name, city
    FROM stops
    WHERE name LIKE ? OR city LIKE ?
    ORDER BY city, name;
"""

STOP_BY_ID_SQL = "SELECT id, name, city FROM stops WHERE id = ?;"

STOP_TRIPS_SQL = """
    SELECT t.id, t.trip_date, t.is_cancelled, r.number
    FROM trips t
    JOIN routes r ON r.id = t.route_id
    WHERE t.stop_from_id = ? OR t.stop_to_id = ?
    ORDER BY t.trip_date;
"""


def stops_list(request):
    """/stops/ — список и поиск остановок."""
    query = request.GET.get("q", "").strip()
    conn = get_connection()
    try:
        if query:
            pattern = f"%{query}%"
            stops = conn.execute(
                SEARCH_STOPS_SQL, [pattern, pattern]
            ).fetchall()
        else:
            stops = conn.execute(ALL_STOPS_SQL).fetchall()
    finally:
        conn.close()
    return render(
        request, "stops_app/list.html", {"stops": stops, "query": query}
    )


def stop_detail(request, stop_id):
    """/stops/<id>/ — страница с кодом 404, если остановки нет."""
    conn = get_connection()
    try:
        stop = conn.execute(STOP_BY_ID_SQL, [stop_id]).fetchone()
        trips = []
        if stop is not None:
            trips = conn.execute(
                STOP_TRIPS_SQL, [stop_id, stop_id]
            ).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "stops_app/detail.html",
        {"stop": stop, "trips": trips},
        status=404 if stop is None else 200,
    )
