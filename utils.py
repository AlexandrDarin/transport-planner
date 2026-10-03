"""Вспомогательные функции ввода с обработкой ошибок."""

from datetime import datetime


def input_int(prompt: str) -> int:
    """Запросить целое число, повторять при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: нужно целое число. Попробуйте снова.")


def input_float(prompt: str) -> float:
    """Запросить число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: нужно число. Попробуйте снова.")


def input_date(prompt: str):
    """Запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: формат даты ДД.ММ.ГГГГ. Попробуйте снова.")