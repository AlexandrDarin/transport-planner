"""Заполнить ORM-базу демонстрационными данными (идемпотентно)."""
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from routes_app.models import Route
from stops_app.models import Stop
from users_app.models import Passenger
from trips_app.models import Trip


class Command(BaseCommand):
    help = 'Добавить демонстрационные маршруты, остановки, пассажиров и поездки'

    @transaction.atomic
    def handle(self, *args, **options):
        routes_data = [
            ('А-101', 'Автобус', '45.00', 35),
            ('А-205', 'Автобус', '55.00', 48),
            ('Т-12', 'Трамвай', '38.00', 27),
            ('Т-18', 'Трамвай', '42.00', 31),
            ('М-1', 'Метро', '60.00', 18),
            ('М-2', 'Метро', '60.00', 22),
            ('Э-7', 'Электробус', '50.00', 40),
            ('Э-9', 'Электробус', '52.00', 44),
            ('МТ-33', 'Маршрутное такси', '70.00', 55),
            ('МТ-41', 'Маршрутное такси', '65.00', 50),
        ]
        routes = []
        for number, kind, price, duration in routes_data:
            route, _ = Route.objects.get_or_create(
                number=number,
                defaults={'transport_type': kind,
                          'base_price': Decimal(price),
                          'travel_time_minutes': duration},
            )
            routes.append(route)

        stop_names = [
            'Центральная площадь', 'Вокзал', 'Университет', 'Парк Победы',
            'Больничный городок', 'Проспект Мира', 'Речной порт',
            'Спортивная', 'Торговый центр', 'Аэропорт', 'Библиотека',
            'Улица Ленина',
        ]
        stops = []
        for index, name in enumerate(stop_names):
            stop, _ = Stop.objects.get_or_create(
                name=name,
                city='Москва' if index < 8 else 'Химки',
            )
            stops.append(stop)

        passengers_data = [
            ('Анна Смирнова', 24, False), ('Иван Иванов', 31, False),
            ('Пётр Петров', 68, True), ('Мария Соколова', 19, False),
            ('Сергей Кузнецов', 45, False), ('Ольга Попова', 72, True),
            ('Дмитрий Васильев', 28, False), ('Елена Новикова', 56, True),
            ('Алексей Морозов', 36, False), ('Наталья Волкова', 63, True),
        ]
        passengers = []
        for name, age, benefits in passengers_data:
            passenger, _ = Passenger.objects.get_or_create(
                name=name,
                defaults={'age': age, 'has_benefits': benefits},
            )
            passengers.append(passenger)

        statuses = [Trip.Status.ACTIVE, Trip.Status.CANCELLED,
                    Trip.Status.COMPLETED]
        created = 0
        today = date.today()
        for index in range(30):
            route = routes[index % len(routes)]
            passenger = passengers[index % len(passengers)]
            origin = stops[index % len(stops)]
            destination = stops[(index + 1) % len(stops)]
            trip_date = today - timedelta(days=index % 12)
            trip, was_created = Trip.objects.get_or_create(
                route=route,
                passenger=passenger,
                origin_stop=origin,
                destination_stop=destination,
                trip_date=trip_date,
                defaults={'status': statuses[index % len(statuses)]},
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            'Демонстрационные данные готовы: '
            f'{Route.objects.count()} маршрутов, '
            f'{Stop.objects.count()} остановок, '
            f'{Passenger.objects.count()} пассажиров, '
            f'{Trip.objects.count()} поездок '
            f'(добавлено новых поездок: {created}).'
        ))
