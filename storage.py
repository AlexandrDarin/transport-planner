"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os


def load_routes(filename: str) -> dict:
    """Загрузить маршруты из JSON. Вернуть {} при ошибке."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {int(k): v for k, v in data.items()}
    except FileNotFoundError:
        print(f"Файл {filename} не найден — стартуем с пустым словарём.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён — стартуем с пустым словарём.")
        return {}


def save_routes(filename: str, routes: dict) -> None:
    """Сохранить маршруты в JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(routes, f, ensure_ascii=False, indent=2)


def load_trips(filename: str) -> list:
    """Загрузить поездки из JSON. Вернуть [] при ошибке."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён — стартуем с пустым списком.")
        return []


def save_trips(filename: str, trips: list) -> None:
    """Сохранить поездки в JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(trips, f, ensure_ascii=False, indent=2)