"""Сервис планирования поездок на общественном транспорте.

Точка входа: меню приложения.
Бизнес-логика вынесена в модули routes.py, trips.py, storage.py, utils.py.
"""

# Импорт функций из модулей проекта.
# Функции is_route_available, calculate_travel_time, calculate_price
# сохранены в main для совместимости с tests/test_main.py из ПР1.
from routes import (
    is_route_available,
    calculate_travel_time,
    calculate_price,
    get_route_status,
    add_route,
    find_routes,
    filter_routes_by_price,
    sort_routes,
    route_statistics,
)
from trips import (
    is_route_free,
    create_trip,
    cancel_trip,
    find_trips_by_user,
    get_trip_summary,
)
from storage import load_routes, save_routes, load_trips, save_trips
from utils import input_int, input_float, input_date


DATA_ROUTES = "data/routes.json"
DATA_TRIPS = "data/trips.json"


def show_routes(routes: dict) -> None:
    """Вывести список маршрутов."""
    if not routes:
        print("Маршрутов пока нет.")
        return
    print(f"{'ID':<4}{'Номер':<10}{'Транспорт':<12}{'Цена':<10}{'Время':<8}")
    for rid, r in routes.items():
        print(f"{rid:<4}{r['number']:<10}{r['transport_type']:<12}"
              f"{r['base_price']:<10}{r['travel_time_minutes']:<8}")


def show_trips(trips: list, routes: dict) -> None:
    """Вывести список поездок."""
    if not trips:
        print("Поездок пока нет.")
        return
    for t in trips:
        route = routes.get(t["route_id"], {})
        print(f"#{t['id']} | {t['date']} | "
              f"маршрут {route.get('number', '?')} | {t['user_name']}")


def menu() -> None:
    """Вывести меню."""
    print("\n=== Сервис планирования поездок ===")
    print("1. Показать маршруты")
    print("2. Найти маршрут")
    print("3. Отобрать по цене")
    print("4. Сортировать по цене")
    print("5. Статистика по маршрутам")
    print("6. Проверить доступность маршрута на дату")
    print("7. Забронировать поездку")
    print("8. Отменить поездку")
    print("9. Показать поездки")
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения."""
    routes = load_routes(DATA_ROUTES)
    trips = load_trips(DATA_TRIPS)

    while True:
        menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_routes(routes)

        elif choice == "2":
            q = input("Подстрока для поиска: ")
            show_routes(find_routes(routes, q))

        elif choice == "3":
            max_price = input_float("Максимальная цена: ")
            show_routes(filter_routes_by_price(routes, max_price))

        elif choice == "4":
            for rid, r in sort_routes(routes):
                print(f"{rid}: {r['number']} — {r['base_price']} руб.")

        elif choice == "5":
            stats = route_statistics(routes)
            print(f"Всего: {stats['count']}, мин: {stats['min_price']}, "
                  f"макс: {stats['max_price']}, средняя: {stats['avg_price']}")

        elif choice == "6":
            route_id = input_int("ID маршрута: ")
            d = input_date("Дата (ДД.ММ.ГГГГ): ")
            free = is_route_free(trips, route_id, d)
            print(get_route_status(free))

        elif choice == "7":
            route_id = input_int("ID маршрута: ")
            user = input("Имя пассажира: ")
            d = input_date("Дата (ДД.ММ.ГГГГ): ")
            trip = create_trip(trips, route_id, d, user)
            if trip:
                save_trips(DATA_TRIPS, trips)
                print(f"Поездка #{trip['id']} создана.")
            else:
                print("Маршрут уже занят на эту дату.")

        elif choice == "8":
            trip_id = input_int("ID поездки: ")
            if cancel_trip(trips, trip_id):
                save_trips(DATA_TRIPS, trips)
                print("Поездка отменена.")
            else:
                print("Поездка не найдена.")

        elif choice == "9":
            show_trips(trips, routes)

        elif choice == "0":
            save_routes(DATA_ROUTES, routes)
            save_trips(DATA_TRIPS, trips)
            print("Данные сохранены. До встречи!")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()