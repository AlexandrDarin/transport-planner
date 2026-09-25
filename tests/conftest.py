import pytest

from models import User, Route, Stop


@pytest.fixture
def sample_user():
    return User(1, "Иван Иванов", 22, has_benefits=False)


@pytest.fixture
def sample_benefit_user():
    return User(2, "Пётр Петров", 70, has_benefits=True)


@pytest.fixture
def sample_route():
    return Route(1, "А-42", "Автобус", 50.0, 35)


@pytest.fixture
def sample_stops():
    return (Stop(1, "Улица Ленина", "Москва"),
            Stop(2, "Площадь Победы", "Москва"))


@pytest.fixture
def temporary_data():
    data = [1, 2, 3, 4, 5]
    yield data
    data.clear()