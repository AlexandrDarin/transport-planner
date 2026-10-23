"""Главная, «О проекте» и страница статистики (SQL: COUNT, GROUP BY)."""

from django.shortcuts import render

from db.database import get_connection

COUNTS_SQL = """
    SELECT
        (SELECT COUNT(*) FROM routes) AS routes,
        (SELECT COUNT(*) FROM stops) AS stops,
        (SELECT COUNT(*) FROM trips) AS trips,
        (SELECT COUNT(*) FROM users) AS users;
"""

SUMMARY_SQL = """
    SELECT
        COUNT(*) AS total_trips,
        SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS active_trips,
        SUM(CASE WHEN is_cancelled = 1 THEN 1 ELSE 0 END) AS cancelled_trips
    FROM trips;
"""

REVENUE_SQL = """
    SELECT SUM(r.base_price * CASE WHEN u.has_benefits = 1
                                   THEN 0.5 ELSE 1 END) AS total
    FROM trips t
    JOIN routes r ON r.id = t.route_id
    JOIN users u ON u.id = t.user_id
    WHERE t.is_cancelled = 0;
"""

ROUTE_STATS_SQL = """
    SELECT r.id, r.number, COUNT(t.id) AS trip_count
    FROM routes r
    LEFT JOIN trips t
           ON t.route_id = r.id AND t.is_cancelled = 0
    GROUP BY r.id, r.number
    ORDER BY trip_count DESC, r.number;
"""

POPULAR_ROUTES_SQL = """
    SELECT r.id, r.number, COUNT(t.id) AS trip_count
    FROM routes r
    JOIN trips t ON t.route_id = r.id
    WHERE t.is_cancelled = 0
    GROUP BY r.id, r.number
    HAVING COUNT(t.id) >= ?
    ORDER BY trip_count DESC, r.number;
"""

TYPE_STATS_SQL = """
    SELECT transport_type,
           COUNT(*) AS routes_count,
           AVG(base_price) AS avg_price
    FROM routes
    GROUP BY transport_type
    ORDER BY routes_count DESC, transport_type;
"""

USER_STATS_SQL = """
    SELECT u.id, u.name,
           COUNT(t.id) AS trips_count,
           COALESCE(SUM(r.base_price * CASE WHEN u.has_benefits = 1
                                            THEN 0.5 ELSE 1 END), 0)
               AS total_spent
    FROM users u
    LEFT JOIN trips t ON t.user_id = u.id AND t.is_cancelled = 0
    LEFT JOIN routes r ON r.id = t.route_id
    GROUP BY u.id, u.name
    ORDER BY total_spent DESC, u.name;
"""

CITY_STATS_SQL = """
    SELECT city, COUNT(*) AS stops_count
    FROM stops
    GROUP BY city
    ORDER BY stops_count DESC, city;
"""

TOP_STOPS_SQL = """
    SELECT s.id, s.name, COUNT(t.id) AS departures
    FROM stops s
    LEFT JOIN trips t
           ON t.stop_from_id = s.id AND t.is_cancelled = 0
    GROUP BY s.id, s.name
    ORDER BY departures DESC, s.name
    LIMIT 3 OFFSET 0;
"""


def index(request):
    """Главная страница: количество записей в таблицах."""
    conn = get_connection()
    try:
        stats = conn.execute(COUNTS_SQL).fetchone()
    finally:
        conn.close()
    return render(request, "homepage/index.html", {"stats": stats})


def about(request):
    """Страница «О проекте»."""
    return render(request, "homepage/about.html")


def statistics(request):
    """Статистика: агрегатные функции, GROUP BY, HAVING, LIMIT."""
    try:
        min_trips = max(0, int(request.GET.get("min_trips", "1")))
    except ValueError:
        min_trips = 1

    conn = get_connection()
    try:
        context = {
            "min_trips": min_trips,
            "summary": conn.execute(SUMMARY_SQL).fetchone(),
            "revenue": conn.execute(REVENUE_SQL).fetchone(),
            "route_stats": conn.execute(ROUTE_STATS_SQL).fetchall(),
            "popular_routes": conn.execute(
                POPULAR_ROUTES_SQL, [min_trips]
            ).fetchall(),
            "type_stats": conn.execute(TYPE_STATS_SQL).fetchall(),
            "user_stats": conn.execute(USER_STATS_SQL).fetchall(),
            "city_stats": conn.execute(CITY_STATS_SQL).fetchall(),
            "top_stops": conn.execute(TOP_STOPS_SQL).fetchall(),
        }
    finally:
        conn.close()
    return render(request, "homepage/statistics.html", context)
