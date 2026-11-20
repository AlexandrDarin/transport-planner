"""Однократный перенос исходных записей ПР7 в таблицы Django ORM."""
import sqlite3
from datetime import date
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify
from routes_app.models import Route
from stops_app.models import Stop
from users_app.models import Passenger
from trips_app.models import Trip


class Command(BaseCommand):
    help = 'Перенести данные из data/transport_planner.sqlite3 в БД Django'

    def add_arguments(self, parser):
        parser.add_argument('--replace', action='store_true', help='Очистить ORM-таблицы перед импортом')

    @transaction.atomic
    def handle(self, *args, **options):
        source = Path(__file__).resolve().parents[3] / 'data' / 'transport_planner.sqlite3'
        if not source.exists():
            raise CommandError(f'Не найдена исходная база: {source}')
        connection = sqlite3.connect(source)
        connection.row_factory = sqlite3.Row
        try:
            if options['replace']:
                Trip.objects.all().delete()
                Route.objects.all().delete()
                Passenger.objects.all().delete()
                Stop.objects.all().delete()
            if Route.objects.exists() or Stop.objects.exists() or Passenger.objects.exists() or Trip.objects.exists():
                raise CommandError('ORM-база уже содержит данные. Для повторного импорта используйте --replace.')
            Route.objects.bulk_create([Route(id=r['id'], number=r['number'], transport_type=r['transport_type'], base_price=r['base_price'], travel_time_minutes=r['travel_time_minutes'], slug=slugify(r['number'], allow_unicode=False) or f"route-{r['id']}") for r in connection.execute('SELECT * FROM routes')])
            Stop.objects.bulk_create([Stop(id=r['id'], name=r['name'], city=r['city']) for r in connection.execute('SELECT * FROM stops')])
            Passenger.objects.bulk_create([Passenger(id=r['id'], name=r['name'], age=r['age'], has_benefits=bool(r['has_benefits'])) for r in connection.execute('SELECT * FROM users')])
            trips = []
            for row in connection.execute('SELECT * FROM trips'):
                trips.append(Trip(id=row['id'], route_id=row['route_id'], passenger_id=row['user_id'], origin_stop_id=row['stop_from_id'], destination_stop_id=row['stop_to_id'], trip_date=date.fromisoformat(row['trip_date']), status=Trip.Status.CANCELLED if row['is_cancelled'] else Trip.Status.ACTIVE))
            Trip.objects.bulk_create(trips)
        finally:
            connection.close()
        self.stdout.write(self.style.SUCCESS(f'Перенесено: маршрутов {Route.objects.count()}, остановок {Stop.objects.count()}, пассажиров {Passenger.objects.count()}, поездок {Trip.objects.count()}.'))
