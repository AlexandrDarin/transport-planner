from models import User
from models.users import (
    add_user, find_user_by_id, find_users_by_name, user_statistics,
)


def test_user_creation():
    user = User(1, "Иван", 22, has_benefits=False)
    assert user.id == 1
    assert user.name == "Иван"
    assert user.age == 22
    assert user.has_benefits is False


def test_user_discount():
    assert User(1, "A", 20, False).get_discount() == 1.0
    assert User(2, "B", 70, True).get_discount() == 0.5


def test_user_str():
    user = User(1, "Иван", 22, False)
    assert "Иван" in str(user)


def test_user_from_data():
    user = User.from_data(
        {"id": 1, "name": "Иван", "age": 22, "has_benefits": False})
    assert user.id == 1
    assert user.name == "Иван"


def test_add_user():
    users = []
    user = add_user(users, "Иван", 22, False)
    assert user.id == 1
    assert len(users) == 1


def test_find_user_by_id():
    users = []
    add_user(users, "Иван", 22, False)
    assert find_user_by_id(users, 1).name == "Иван"
    assert find_user_by_id(users, 99) is None


def test_find_users_by_name():
    users = []
    add_user(users, "Иван Иванов", 22, False)
    add_user(users, "Пётр Петров", 70, True)
    assert len(find_users_by_name(users, "иван")) == 1


def test_user_statistics():
    users = []
    add_user(users, "Иван", 20, False)
    add_user(users, "Пётр", 30, False)
    stats = user_statistics(users)
    assert stats["count"] == 2
    assert stats["avg_age"] == 25.0