from datetime import date, datetime          # импорт классов date и datetime из модуля datetime

# ----- Пользователь -----
user_name = "Иван Иванов"                    # имя пассажира, тип str (строка)
user_age = 22                                # возраст пассажира, тип int (целое число)
has_benefits = False                         # наличие льгот, тип bool (True/False)

# ----- Маршрут -----
route_number = "А-42"                        # номер маршрута, тип str
route_type = "Автобус"                       # вид транспорта, тип str
travel_time_minutes = 35                     # время в пути без остановок, тип int, в минутах
base_price = 50.0                            # базовая стоимость проезда, тип float, в рублях

# ----- Остановки -----
stop_from = "Улица Ленина"                   # начальная остановка, тип str
stop_to = "Площадь Победы"                   # конечная остановка, тип str
stops_count = 8                              # количество остановок на пути, тип int

# ----- Поездка -----
trip_date = date(2026, 9, 15)                # дата поездки: год=2026, месяц=9, день=15; тип date
departure_time = datetime(2026, 9, 15, 8, 30)  # дата+время отправления 08:30; тип datetime


# Функция 1: проверка доступности маршрута
def is_route_available(route_number, stop_from, stop_to):   # объявление функции; 3 параметра
    if route_number and stop_from and stop_to:              # проверяем: все три значения непустые (логическое И)
        return True                                         # если да — возвращаем True (маршрут доступен)
    return False                                            # иначе возвращаем False (недоступен)


# Функция 2: расчёт времени поездки
def calculate_travel_time(travel_time_minutes, stops_count):   # объявление функции; 2 параметра (int)
    total_time = travel_time_minutes + stops_count             # складываем время в пути и число остановок
    return total_time                                          # возвращаем результат (int)


# Функция 3: расчёт стоимости проезда
def calculate_price(base_price, has_benefits):   # объявление функции; параметры: цена (float) и флаг льгот (bool)
    if has_benefits:                             # если льготы есть (True)
        return base_price * 0.5                  # возвращаем половину цены (скидка 50%)
    return base_price                            # иначе возвращаем полную цену


# Функция 4: сводка о поездке
def get_trip_summary(user_name, route_number, stop_from, stop_to,
                     travel_time, price):        # объявление функции; 6 параметров для формирования текста
    return (                                     # возвращаем многострочную строку через f-строки
        f"Пассажир: {user_name}\n"               # \n — символ переноса строки; подставляем имя
        f"Маршрут: {route_number}\n"             # подставляем номер маршрута
        f"Откуда: {stop_from}\n"                 # подставляем начальную остановку
        f"Куда: {stop_to}\n"                     # подставляем конечную остановку
        f"Время в пути: ~{travel_time} мин.\n"   # подставляем рассчитанное время
        f"Стоимость: {price:.2f} руб."           # :.2f — формат float с 2 знаками после запятой
    )


def main():                                      # главная функция - точка входа в сценарий
    print("=== Сервис планирования поездок ===") # печатаем заголовок программы
    print(f"Дата поездки: {trip_date}")          # печатаем дату поездки
    print(f"Время отправления: {departure_time.strftime('%H:%M')}")   # печатаем только часы:минуты
    print()                                       # печатаем пустую строку для отступа

    available = is_route_available(route_number, stop_from, stop_to)  # вызываем функцию 1, результат в available (bool)
    if not available:                             # если маршрут недоступен (not True)
        print("Маршрут недоступен для указанных остановок.")  # сообщение об ошибке
        return                                    # выходим из main, дальше не идём

    travel_time = calculate_travel_time(travel_time_minutes, stops_count)  # вызов функции 2; результат (int) в travel_time
    price = calculate_price(base_price, has_benefits)                      # вызов функции 3; результат (float) в price

    print(get_trip_summary(                       # вызов функции 4 и печать её результата
        user_name, route_number, stop_from, stop_to, travel_time, price    # передаём 6 аргументов
    ))


if __name__ == "__main__":   # проверка: файл запущен напрямую, а не импортирован?
    main()                   # если да — запускаем main()