"""Страницы маршрутов; данные выбираются SQL-запросами SQLite."""
from django.shortcuts import render
from db.database import get_connection


def routes_list(request):
    query = request.GET.get("q", "").strip()
    connection = get_connection()
    try:
        if query:
            routes = connection.execute("SELECT * FROM routes WHERE number LIKE ? OR transport_type LIKE ? ORDER BY number", (f"%{query}%", f"%{query}%")).fetchall()
        else:
            routes = connection.execute("SELECT * FROM routes ORDER BY number").fetchall()
        stats = connection.execute("SELECT COUNT(*) AS count, MIN(base_price) AS min_price, MAX(base_price) AS max_price, AVG(base_price) AS avg_price FROM routes").fetchone()
    finally:
        connection.close()
    return render(request, "routes_app/list.html", {"page_title": "Маршруты", "active": "routes", "routes": routes, "query": query, "stats": stats})


def route_detail(request, route_id: int):
    connection = get_connection()
    try:
        route = connection.execute("SELECT * FROM routes WHERE id = ?", (route_id,)).fetchone()
        if route:
            trips = connection.execute("""SELECT t.*, u.name AS passenger FROM trips t JOIN users u ON u.id=t.user_id WHERE t.route_id=? ORDER BY t.trip_date""", (route_id,)).fetchall()
    finally:
        connection.close()
    if not route:
        from django.http import Http404
        raise Http404("Маршрут не найден")
    return render(request, "routes_app/detail.html", {"page_title": f"Маршрут {route['number']}", "active": "routes", "route": route, "trips": trips})
