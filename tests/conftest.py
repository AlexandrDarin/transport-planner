import pytest


@pytest.fixture
def sample_route():
    """Маршрут с базовыми параметрами."""
    return {
        "number": "А-42",
        "transport_type": "Автобус",
        "base_price": 50.0,
        "travel_time_minutes": 35,
        "stops_count": 8,
    }


@pytest.fixture
def sample_stops():
    """Пара остановок."""
    return ("Улица Ленина", "Площадь Победы")


@pytest.fixture
def temporary_data():
    """Фикстура с очисткой после теста."""
    data = [1, 2, 3, 4, 5]
    print("Данные подготовлены:", data)
    yield data
    data.clear()
    print(f"{data} - пусто, данные очищены!")