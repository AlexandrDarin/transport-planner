"""Функции для работы с пользователями."""


def add_user(users: list[dict], name: str, age: int,
             has_benefits: bool) -> int:
    """Добавить пользователя в список users и вернуть его id."""
    user_id = max((u["id"] for u in users), default=0) + 1
    users.append({
        "id": user_id,
        "name": name,
        "age": age,
        "has_benefits": has_benefits,
    })
    return user_id


def find_user_by_id(users: list[dict], user_id: int) -> dict | None:
    """Найти пользователя по id. None — если нет."""
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def find_users_by_name(users: list[dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке в имени."""
    q = query.lower()
    return [u for u in users if q in u["name"].lower()]


def get_user_discount(user: dict) -> float:
    """Коэффициент скидки: 0.5 при льготах, иначе 1.0."""
    return 0.5 if user["has_benefits"] else 1.0


def user_statistics(users: list[dict]) -> dict:
    """Статистика по пользователям: количество и средний возраст."""
    if not users:
        return {"count": 0, "avg_age": 0}
    ages = [u["age"] for u in users]
    return {
        "count": len(users),
        "avg_age": round(sum(ages) / len(ages), 2),
    }