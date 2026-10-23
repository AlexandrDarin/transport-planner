"""Страницы маршрутов: данные берутся из SQLite параметризованными SQL."""

from django.shortcuts import render

from db.database import get_connection

ROUTE_COLUMNS = "id, number, transport_type, base_price, travel_time_minutes"

ALL_ROUTES_SQL = f"SELECT {ROUTE_COLUMNS} FROM routes ORDER BY number;"

SEARCH_ROUTES_SQL = f"""
    SELECT {ROUTE_COLUMNS}
    FROM routes
    WHERE number LIKE ? OR transport_type LIKE ?
    ORDER BY number;
"""

PRICE_ROUTES_SQL = f"""
    SELECT {ROUTE_COLUMNS}
    FROM routes
    WHERE base_price <= ?
    ORDER BY base_price;
"""

ROUTE_STATS_SQL = """
    SELECT COUNT(*) AS count,
           MIN(base_price) AS min_price,
           MAX(base_price) AS max_price,
           AVG(base_price) AS avg_price
    FROM routes;
"""

ROUTE_BY_ID_SQL = f"SELECT {ROUTE_COLUMNS} FROM routes WHERE id = ?;"

ROUTE_TRIPS_SQL = """
    SELECT t.id, t.trip_date, t.is_cancelled, u.name AS passenger
    FROM trips t
    JOIN users u ON u.id = t.user_id
    WHERE t.route_id = ?
    ORDER BY t.trip_date;
"""

FREE_ROUTES_SQL = f"""
    SELECT {ROUTE_COLUMNS}
    FROM routes
    WHERE id NOT IN (
        SELECT route_id
        FROM trips
        WHERE trip_date = ?
          AND is_cancelled = 0
    )
    ORDER BY number;
"""


def routes_list(request):
    """/routes/ — список, поиск по тексту и фильтр по цене."""
    query = request.GET.get("q", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    conn = get_connection()
    try:
        if query:
            pattern = f"%{query}%"
            routes = conn.execute(
                SEARCH_ROUTES_SQL, [pattern, pattern]
            ).fetchall()
        elif max_price:
            try:
                routes = conn.execute(
                    PRICE_ROUTES_SQL, [float(max_price)]
                ).fetchall()
            except ValueError:
                routes = conn.execute(ALL_ROUTES_SQL).fetchall()
        else:
            routes = conn.execute(ALL_ROUTES_SQL).fetchall()
        stats = conn.execute(ROUTE_STATS_SQL).fetchone()
    finally:
        conn.close()

    context = {
        "routes": routes,
        "stats": stats,
        "query": query,
        "max_price": max_price,
    }
    return render(request, "routes_app/list.html", context)


def route_detail(request, route_id):
    """/routes/<id>/ — страница с кодом 404, если маршрута нет."""
    conn = get_connection()
    try:
        route = conn.execute(ROUTE_BY_ID_SQL, [route_id]).fetchone()
        trips = []
        if route is not None:
            trips = conn.execute(ROUTE_TRIPS_SQL, [route_id]).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "routes_app/detail.html",
        {"route": route, "trips": trips},
        status=404 if route is None else 200,
    )


def available_routes(request):
    """/routes/available/?date=YYYY-MM-DD — свободные маршруты на дату."""
    trip_date = request.GET.get("date", "").strip()
    routes = []
    if trip_date:
        conn = get_connection()
        try:
            routes = conn.execute(FREE_ROUTES_SQL, [trip_date]).fetchall()
        finally:
            conn.close()

    return render(
        request,
        "routes_app/available.html",
        {"routes": routes, "trip_date": trip_date},
    )
