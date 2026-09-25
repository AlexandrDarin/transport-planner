"""Сервис планирования поездок на общественном транспорте.

Точка входа: меню приложения.
Объектная модель — в пакете models.
"""

from typing import List

# Совместимость с тестами ПР1/ПР2
from models.routes import (
    is_route_available,
    calculate_travel_time,
    calculate_price,
    get_route_status,
    find_routes,
    filter_routes_by_price,
    sort_routes,
    route_statistics,
)
from models.trips import (
    is_route_free,
    create_trip,
    cancel_trip,
    find_trips_by_user,
    get_trip_summary,
)
from models.users import (
    add_user,
    find_user_by_id,
    find_users_by_name,
    user_statistics,
)
from models.stops import (
    add_stop,
    find_stop_by_id,
    find_stops_by_name,
    filter_stops_by_city,
    sort_stops_by_name,
)
from models import User, Route, Stop, Trip

from storage import (
    load_users, save_users,
    load_routes, save_routes,
    load_stops, save_stops,
    load_trips, save_trips,
)
from utils import input_int, input_float, input_date


DATA_USERS = "data/users.json"
DATA_ROUTES = "data/routes.json"
DATA_STOPS = "data/stops.json"
DATA_TRIPS = "data/trips.json"


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователей пока нет.")
        return
    for u in users:
        print(f"{u.id:<4}{u.name:<20}{u.age:<10}{str(u.has_benefits):<8}")


def show_stops(stops: List[Stop]) -> None:
    """Вывести список остановок."""
    if not stops:
        print("Остановок пока нет.")
        return
    for s in stops:
        print(f"{s.id:<4}{s.name:<25}{s.city:<15}")


def show_routes(routes: List[Route]) -> None:
    """Вывести список маршрутов."""
    if not routes:
        print("Маршрутов пока нет.")
        return
    for r in routes:
        print(f"{r.id:<4}{r.number:<10}{r.transport_type:<12}"
              f"{r.base_price:<10}{r.travel_time_minutes:<8}")


def show_trips(trips: List[Trip]) -> None:
    """Вывести список поездок."""
    if not trips:
        print("Поездок пока нет.")
        return
    for t in trips:
        print(t)


def menu() -> None:
    """Вывести меню."""
    print("\n=== Сервис планирования поездок ===")
    print("1. Показать маршруты")
    print("2. Найти маршрут")
    print("3. Отобрать по цене")
    print("4. Сортировать по цене")
    print("5. Статистика по маршрутам")
    print("6. Показать пользователей")
    print("7. Найти пользователя")
    print("8. Показать остановки")
    print("9. Найти остановку")
    print("10. Проверить доступность маршрута на дату")
    print("11. Забронировать поездку")
    print("12. Отменить поездку")
    print("13. Показать поездки")
    print("0. Выход")


def create_new_trip(trips: List[Trip], routes: List[Route],
                    users: List[User], stops: List[Stop]) -> None:
    """Сценарий создания поездки через меню."""
    route_id = input_int("ID маршрута: ")
    route = next((r for r in routes if r.id == route_id), None)
    if route is None:
        print("Маршрут не найден.")
        return

    user_id = input_int("ID пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return

    stop_from_id = input_int("ID остановки отправления: ")
    stop_from = find_stop_by_id(stops, stop_from_id)
    if stop_from is None:
        print("Остановка отправления не найдена.")
        return

    stop_to_id = input_int("ID остановки назначения: ")
    stop_to = find_stop_by_id(stops, stop_to_id)
    if stop_to is None:
        print("Остановка назначения не найдена.")
        return

    d = input_date("Дата (ДД.ММ.ГГГГ): ")
    trip = create_trip(trips, route, user, stop_from, stop_to, d)
    if trip:
        save_trips(DATA_TRIPS, trips)
        print(f"Поездка #{trip.id} создана.")
    else:
        print("Маршрут уже занят на эту дату.")


def main() -> None:
    """Точка запуска приложения."""
    users = load_users(DATA_USERS)
    routes = load_routes(DATA_ROUTES)
    stops = load_stops(DATA_STOPS)
    trips = load_trips(DATA_TRIPS, routes, users, stops)

    while True:
        menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_routes(routes)
        elif choice == "2":
            show_routes(find_routes(routes, input("Подстрока: ")))
        elif choice == "3":
            show_routes(filter_routes_by_price(
                routes, input_float("Максимальная цена: ")))
        elif choice == "4":
            for r in sort_routes(routes):
                print(f"{r.id}: {r.number} — {r.base_price} руб.")
        elif choice == "5":
            stats = route_statistics(routes)
            print(f"Всего: {stats['count']}, мин: {stats['min_price']}, "
                  f"макс: {stats['max_price']}, средняя: {stats['avg_price']}")
        elif choice == "6":
            show_users(users)
        elif choice == "7":
            show_users(find_users_by_name(users, input("Подстрока: ")))
        elif choice == "8":
            show_stops(stops)
        elif choice == "9":
            show_stops(find_stops_by_name(stops, input("Подстрока: ")))
        elif choice == "10":
            route_id = input_int("ID маршрута: ")
            route = next((r for r in routes if r.id == route_id), None)
            if route is None:
                print("Маршрут не найден.")
                continue
            d = input_date("Дата (ДД.ММ.ГГГГ): ")
            print(get_route_status(is_route_free(trips, route, d)))
        elif choice == "11":
            create_new_trip(trips, routes, users, stops)
        elif choice == "12":
            trip_id = input_int("ID поездки: ")
            if cancel_trip(trips, trip_id):
                save_trips(DATA_TRIPS, trips)
                print("Поездка отменена.")
            else:
                print("Поездка не найдена.")
        elif choice == "13":
            show_trips(trips)
        elif choice == "0":
            save_users(DATA_USERS, users)
            save_routes(DATA_ROUTES, routes)
            save_stops(DATA_STOPS, stops)
            save_trips(DATA_TRIPS, trips)
            print("Данные сохранены. До встречи!")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()