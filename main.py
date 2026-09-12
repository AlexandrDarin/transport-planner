from datetime import date, datetime   # импорт классов date и datetime из модуля datetime

# ----- Пользователь -----
user_name = "Иван Иванов"             # имя пассажира, строка (str)
user_age = 22                         # возраст, целое число (int)
has_benefits = False                  # есть ли льготы, логический тип (bool)

# ----- Маршрут -----
route_number = "А-42"                 # номер маршрута, строка
route_type = "Автобус"                # вид транспорта, строка
travel_time_minutes = 35              # время в пути без остановок, int (минуты)
base_price = 50.0                     # базовая стоимость проезда, float (рубли)

# ----- Остановки -----
stop_from = "Улица Ленина"            # начальная остановка
stop_to = "Площадь Победы"            # конечная остановка
stops_count = 8                       # количество остановок на пути, int

# ----- Поездка -----
trip_date = date(2026, 9, 15)         # дата поездки: год, месяц, день
departure_time = datetime(2026, 9, 15, 8, 30)   # дата и время отправления: 08:30


# Функция 1: проверка доступности маршрута
def is_route_available(route_number, stop_from, stop_to):   # объявление функции с 3 параметрами
    if route_number and stop_from and stop_to:              # все три непустые? (логическое И)
        return True                                         # маршрут доступен
    return False                                            # хотя бы одно пустое — недоступен


# Функция 2: расчёт времени поездки
def calculate_travel_time(travel_time_minutes, stops_count):   # параметры: время и число остановок
    total_time = travel_time_minutes + stops_count             # складываем: 1 мин на остановку
    return total_time                                          # возвращаем итог (int)


# Функция 3: расчёт стоимости проезда
def calculate_price(base_price, has_benefits):   # параметры: цена и флаг льгот
    if has_benefits:                             # если льготы есть (True)
        return base_price * 0.5                  # скидка 50%
    return base_price                            # иначе — полная цена


# Функция 4: сводка о поездке
def get_trip_summary(user_name, route_number, stop_from, stop_to,
                     travel_time, price):        # 6 параметров для формирования текста
    return (                                     # возвращаем многострочный текст через f-строки
        f"Пассажир: {user_name}\n"               # \n — перенос строки
        f"Маршрут: {route_number}\n"
        f"Откуда: {stop_from}\n"
        f"Куда: {stop_to}\n"
        f"Время в пути: ~{travel_time} мин.\n"
        f"Стоимость: {price:.2f} руб."           # :.2f — 2 знака после запятой
    )


def main():                                      # главная функция — точка входа в сценарий
    print("=== Сервис планирования поездок ===") # заголовок
    print(f"Дата поездки: {trip_date}")          # печатаем дату
    print(f"Время отправления: {departure_time.strftime('%H:%M')}")   # только часы:минуты
    print()                                       # пустая строка для отступа

    available = is_route_available(route_number, stop_from, stop_to)  # вызываем функцию 1
    if not available:                             # если маршрут недоступен
        print("Маршрут недоступен для указанных остановок.")
        return                                    # выходим из функции

    travel_time = calculate_travel_time(travel_time_minutes, stops_count)  # вызываем функцию 2
    price = calculate_price(base_price, has_benefits)                      # вызываем функцию 3

    print(get_trip_summary(                       # вызываем функцию 4 и печатаем результат
        user_name, route_number, stop_from, stop_to, travel_time, price
    ))


if __name__ == "__main__":   # этот блок выполнится, только если файл запущен напрямую
    main()                   # (а не импортирован как модуль) — запуск сценария