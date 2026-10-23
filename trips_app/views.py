"""Страницы поездок с JOIN-запросами к SQLite."""
from django.shortcuts import render
from db.database import get_connection

TRIP_SELECT = """SELECT t.*, r.number AS route_number, r.transport_type, r.base_price, u.name AS passenger, u.has_benefits, sf.name AS origin, st.name AS destination, ROUND(r.base_price * CASE WHEN u.has_benefits=1 THEN 0.5 ELSE 1 END, 2) AS price FROM trips t JOIN routes r ON r.id=t.route_id JOIN users u ON u.id=t.user_id JOIN stops sf ON sf.id=t.stop_from_id JOIN stops st ON st.id=t.stop_to_id"""


def trips_list(request):
    status = request.GET.get("status", "all")
    connection = get_connection()
    try:
        if status == "active":
            trips = connection.execute(TRIP_SELECT + " WHERE t.is_cancelled=0 ORDER BY t.trip_date DESC").fetchall()
        elif status == "cancelled":
            trips = connection.execute(TRIP_SELECT + " WHERE t.is_cancelled=1 ORDER BY t.trip_date DESC").fetchall()
        else:
            trips = connection.execute(TRIP_SELECT + " ORDER BY t.trip_date DESC").fetchall()
        stats = connection.execute("SELECT COUNT(*) AS total, SUM(CASE WHEN is_cancelled=0 THEN 1 ELSE 0 END) AS active, SUM(CASE WHEN is_cancelled=1 THEN 1 ELSE 0 END) AS cancelled FROM trips").fetchone()
    finally:
        connection.close()
    return render(request, "trips_app/list.html", {"page_title": "Поездки", "active": "trips", "trips": trips, "stats": stats, "status": status})


def trip_detail(request, trip_id: int):
    connection = get_connection()
    try:
        trip = connection.execute(TRIP_SELECT + " WHERE t.id=?", (trip_id,)).fetchone()
    finally:
        connection.close()
    if not trip:
        from django.http import Http404
        raise Http404("Поездка не найдена")
    return render(request, "trips_app/detail.html", {"page_title": f"Поездка №{trip_id}", "active": "trips", "trip": trip})
