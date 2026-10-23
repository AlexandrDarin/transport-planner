"""Страницы поездок: JOIN пяти таблиц в SQLite."""

from django.shortcuts import render

from db.database import get_connection

TRIP_SELECT = """
    SELECT
        t.id, t.route_id, t.user_id, t.stop_from_id, t.stop_to_id,
        t.trip_date, t.is_cancelled,
        r.number AS route_number, r.transport_type, r.base_price,
        u.name AS passenger, u.has_benefits,
        sf.name AS origin, st.name AS destination,
        ROUND(r.base_price * CASE WHEN u.has_benefits = 1
                                  THEN 0.5 ELSE 1 END, 2) AS price
    FROM trips t
    JOIN routes r ON r.id = t.route_id
    JOIN users u ON u.id = t.user_id
    JOIN stops sf ON sf.id = t.stop_from_id
    JOIN stops st ON st.id = t.stop_to_id
"""

ORDER_BY = " ORDER BY t.trip_date DESC, t.id DESC;"

ALL_TRIPS_SQL = TRIP_SELECT + ORDER_BY
TRIPS_BY_STATUS_SQL = TRIP_SELECT + " WHERE t.is_cancelled = ?" + ORDER_BY
TRIP_BY_ID_SQL = TRIP_SELECT + " WHERE t.id = ?;"

TRIP_COUNTS_SQL = """
    SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS active,
        SUM(CASE WHEN is_cancelled = 1 THEN 1 ELSE 0 END) AS cancelled
    FROM trips;
"""

STATUS_FLAGS = {"active": 0, "cancelled": 1}


def trips_list(request):
    """/trips/ — все поездки или отфильтрованные по статусу."""
    status = request.GET.get("status", "all")
    if status not in STATUS_FLAGS:
        status = "all"

    conn = get_connection()
    try:
        if status == "all":
            trips = conn.execute(ALL_TRIPS_SQL).fetchall()
        else:
            trips = conn.execute(
                TRIPS_BY_STATUS_SQL, [STATUS_FLAGS[status]]
            ).fetchall()
        stats = conn.execute(TRIP_COUNTS_SQL).fetchone()
    finally:
        conn.close()

    context = {"trips": trips, "stats": stats, "status": status}
    return render(request, "trips_app/list.html", context)


def trip_detail(request, trip_id):
    """/trips/<id>/ — страница с кодом 404, если поездки нет."""
    conn = get_connection()
    try:
        trip = conn.execute(TRIP_BY_ID_SQL, [trip_id]).fetchone()
    finally:
        conn.close()

    return render(
        request,
        "trips_app/detail.html",
        {"trip": trip},
        status=404 if trip is None else 200,
    )
