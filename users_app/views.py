"""Страницы пассажиров на основе SQLite."""

from django.shortcuts import render

from db.database import get_connection

ALL_USERS_SQL = """
    SELECT id, name, age, has_benefits
    FROM users
    ORDER BY name;
"""

SEARCH_USERS_SQL = """
    SELECT id, name, age, has_benefits
    FROM users
    WHERE name LIKE ?
    ORDER BY name;
"""

USER_BY_ID_SQL = """
    SELECT id, name, age, has_benefits
    FROM users
    WHERE id = ?;
"""

USER_TRIPS_SQL = """
    SELECT t.id, t.trip_date, t.is_cancelled, r.number
    FROM trips t
    JOIN routes r ON r.id = t.route_id
    WHERE t.user_id = ?
    ORDER BY t.trip_date DESC;
"""

USER_SPENT_SQL = """
    SELECT COALESCE(SUM(r.base_price * CASE WHEN u.has_benefits = 1
                                            THEN 0.5 ELSE 1 END), 0) AS total
    FROM trips t
    JOIN routes r ON r.id = t.route_id
    JOIN users u ON u.id = t.user_id
    WHERE t.user_id = ? AND t.is_cancelled = 0;
"""


def users_list(request):
    """/users/ — список и поиск пассажиров."""
    query = request.GET.get("q", "").strip()
    conn = get_connection()
    try:
        if query:
            users = conn.execute(
                SEARCH_USERS_SQL, [f"%{query}%"]
            ).fetchall()
        else:
            users = conn.execute(ALL_USERS_SQL).fetchall()
    finally:
        conn.close()
    return render(
        request, "users_app/list.html", {"users": users, "query": query}
    )


def user_detail(request, user_id):
    """/users/<id>/ — страница с кодом 404, если пользователя нет.

    В контексте ключ user_item (а не user), чтобы не конфликтовать
    с переменной user контекстного процессора auth.
    """
    conn = get_connection()
    try:
        user = conn.execute(USER_BY_ID_SQL, [user_id]).fetchone()
        trips = []
        spent = None
        if user is not None:
            trips = conn.execute(USER_TRIPS_SQL, [user_id]).fetchall()
            spent = conn.execute(USER_SPENT_SQL, [user_id]).fetchone()
    finally:
        conn.close()

    return render(
        request,
        "users_app/detail.html",
        {"user_item": user, "trips": trips, "spent": spent},
        status=404 if user is None else 200,
    )
