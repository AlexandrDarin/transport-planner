"""Класс User и функции работы с коллекцией пользователей."""

from __future__ import annotations
from typing import List


class User:
    """Пользователь сервиса планирования поездок."""

    def __init__(self, user_id: int, name: str, age: int,
                 has_benefits: bool = False) -> None:
        self.id = user_id
        self.name = name
        self.age = age
        self.has_benefits = has_benefits

    def get_discount(self) -> float:
        """Коэффициент скидки: 0.5 при льготах, иначе 1.0."""
        return 0.5 if self.has_benefits else 1.0

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из набора данных."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            age=data["age"],
            has_benefits=data["has_benefits"],
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "has_benefits": self.has_benefits,
        }

    def __str__(self) -> str:
        return f"{self.name}, {self.age} лет, льготы: {self.has_benefits}"


# ---------- Функции работы с коллекцией пользователей ----------

def add_user(users: List[User], name: str, age: int,
             has_benefits: bool) -> User:
    """Создать пользователя и добавить в коллекцию."""
    user_id = max((u.id for u in users), default=0) + 1
    user = User(user_id, name, age, has_benefits)
    users.append(user)
    return user


def find_user_by_id(users: List[User], user_id: int) -> User | None:
    """Найти пользователя по id."""
    for u in users:
        if u.id == user_id:
            return u
    return None


def find_users_by_name(users: List[User], query: str) -> List[User]:
    """Найти пользователей по подстроке в имени."""
    q = query.lower()
    return [u for u in users if q in u.name.lower()]


def user_statistics(users: List[User]) -> dict:
    """Статистика по пользователям."""
    if not users:
        return {"count": 0, "avg_age": 0}
    ages = [u.age for u in users]
    return {
        "count": len(users),
        "avg_age": round(sum(ages) / len(ages), 2),
    }