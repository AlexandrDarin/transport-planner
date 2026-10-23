"""Страницы остановок на основе SQLite."""
from django.shortcuts import render
from db.database import get_connection


def stops_list(request):
    query = request.GET.get("q", "").strip()
    connection = get_connection()
    try:
        if query:
            stops = connection.execute("SELECT * FROM stops WHERE name LIKE ? OR city LIKE ? ORDER BY city, name", (f"%{query}%", f"%{query}%")).fetchall()
        else:
            stops = connection.execute("SELECT * FROM stops ORDER BY city, name").fetchall()
    finally:
        connection.close()
    return render(request, "stops_app/list.html", {"page_title": "Остановки", "active": "stops", "stops": stops, "query": query})


def stop_detail(request, stop_id: int):
    connection = get_connection()
    try:
        stop = connection.execute("SELECT * FROM stops WHERE id=?", (stop_id,)).fetchone()
        trips = connection.execute("""SELECT t.id, t.trip_date, t.is_cancelled, r.number FROM trips t JOIN routes r ON r.id=t.route_id WHERE t.stop_from_id=? OR t.stop_to_id=? ORDER BY t.trip_date""", (stop_id, stop_id)).fetchall() if stop else []
    finally:
        connection.close()
    if not stop:
        from django.http import Http404
        raise Http404("Остановка не найдена")
    return render(request, "stops_app/detail.html", {"page_title": stop["name"], "active": "stops", "stop": stop, "trips": trips})
