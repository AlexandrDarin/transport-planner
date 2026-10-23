"""Главная страница и сведения о проекте."""
from django.shortcuts import render
from db.database import get_connection


def index(request):
    connection = get_connection()
    try:
        stats = {"routes": connection.execute("SELECT COUNT(*) FROM routes").fetchone()[0],
                 "stops": connection.execute("SELECT COUNT(*) FROM stops").fetchone()[0],
                 "trips": connection.execute("SELECT COUNT(*) FROM trips").fetchone()[0],
                 "users": connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]}
    finally:
        connection.close()
    return render(request, "homepage/index.html", {"page_title": "Сервис планирования поездок", "active": "home", "stats": stats})


def about(request):
    return render(request, "homepage/about.html", {"page_title": "О проекте", "active": "about"})


def statistics(request):
    """Статистика по поездкам и маршрутам через GROUP BY / HAVING."""
    threshold = request.GET.get("min_trips", "0")
    try:
        threshold_value = max(0, int(threshold))
    except ValueError:
        threshold_value = 0
    connection = get_connection()
    try:
        route_stats = connection.execute("""SELECT r.id, r.number, COUNT(t.id) AS trip_count FROM routes r LEFT JOIN trips t ON t.route_id=r.id GROUP BY r.id, r.number ORDER BY trip_count DESC, r.number""").fetchall()
        popular_routes = connection.execute("""SELECT r.id, r.number, COUNT(t.id) AS trip_count FROM routes r JOIN trips t ON t.route_id=r.id GROUP BY r.id, r.number HAVING COUNT(t.id) > ? ORDER BY trip_count DESC""", (threshold_value,)).fetchall()
        summary = connection.execute("""SELECT COUNT(*) AS total_trips, SUM(CASE WHEN is_cancelled=0 THEN 1 ELSE 0 END) AS active_trips, SUM(CASE WHEN is_cancelled=1 THEN 1 ELSE 0 END) AS cancelled_trips FROM trips""").fetchone()
    finally:
        connection.close()
    return render(request, "homepage/statistics.html", {"page_title": "Статистика", "active": "statistics", "route_stats": route_stats, "popular_routes": popular_routes, "summary": summary, "min_trips": threshold_value})
