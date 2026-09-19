import os
import sys

import pytest

# Добавляем корень проекта в sys.path, чтобы импортировать main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import (
    is_route_available,
    calculate_travel_time,
    calculate_price,
)


# ============================================================
# Задание 1. Простые тесты
# ============================================================

def test_add_route_available():
    assert is_route_available("А-42", "Улица Ленина", "Площадь Победы") is True


def test_add_route_unavailable():
    assert is_route_available("", "Улица Ленина", "Площадь Победы") is False


def test_calculate_travel_time():
    assert calculate_travel_time(35, 8) == 43


def test_calculate_price_without_benefits():
    assert calculate_price(50.0, False) == 50.0


def test_calculate_price_with_benefits():
    assert calculate_price(50.0, True) == 25.0


def test_type_of_travel_time():
    assert isinstance(calculate_travel_time(35, 8), int)


# ============================================================
# Задание 2. Маркировки, параметризация, фикстуры
# ============================================================

@pytest.mark.smoke
def test_route_available(sample_route, sample_stops):
    stop_from, stop_to = sample_stops
    assert is_route_available(
        sample_route["number"], stop_from, stop_to
    ) is True


@pytest.mark.regression
def test_travel_time(sample_route):
    assert calculate_travel_time(
        sample_route["travel_time_minutes"],
        sample_route["stops_count"],
    ) == 43


@pytest.mark.skip(reason="Тест устарел и требует переработки")
def test_old_functionality():
    assert False


@pytest.mark.xfail(reason="Баг в API, исправят в версии 2.5")
def test_broken_feature():
    assert calculate_travel_time(2, 3) == 6


@pytest.mark.parametrize("base_price, has_benefits, expected", [
    (50.0,  False, 50.0),
    (50.0,  True,  25.0),
    (100.0, False, 100.0),
    (100.0, True,  50.0),
])
def test_calculate_price_parametrized(base_price, has_benefits, expected):
    assert calculate_price(base_price, has_benefits) == expected


@pytest.mark.parametrize("minutes, stops, expected", [
    (35, 8, 43),
    (10, 0, 10),
    (0,  5,  5),
])
def test_travel_time_parametrized(minutes, stops, expected):
    assert calculate_travel_time(minutes, stops) == expected


def test_data_processing(temporary_data):
    print("Начало теста - данные:", temporary_data)
    assert sum(temporary_data) == 15
    assert len(temporary_data) == 5
    temporary_data.append(6)
    print("Данные изменены:", temporary_data)