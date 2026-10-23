"""Страницы пассажиров на основе SQLite."""
from django.shortcuts import render
from db.database import get_connection


def users_list(request):
    query = request.GET.get("q", "").strip()
    connection = get_connection()
    try:
        if query:
            users = connection.execute("SELECT * FROM users WHERE name LIKE ? ORDER BY name", (f"%{query}%",)).fetchall()
        else:
            users = connection.execute("SELECT * FROM users ORDER BY name").fetchall()
    finally:
        connection.close()
    return render(request, "users_app/list.html", {"page_title": "Пользователи", "active": "users", "users": users, "query": query})


def user_detail(request, user_id: int):
    connection = get_connection()
    try:
        user = connection.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        trips = connection.execute("SELECT t.id, t.trip_date, t.is_cancelled, r.number FROM trips t JOIN routes r ON r.id=t.route_id WHERE t.user_id=? ORDER BY t.trip_date DESC", (user_id,)).fetchall() if user else []
    finally:
        connection.close()
    if not user:
        from django.http import Http404
        raise Http404("Пользователь не найден")
    return render(request, "users_app/detail.html", {"page_title": user["name"], "active": "users", "user": user, "trips": trips})
