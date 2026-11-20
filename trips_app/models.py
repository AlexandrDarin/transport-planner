from django.db import models


class TripQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Trip.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=Trip.Status.CANCELLED)

    def completed(self):
        return self.filter(status=Trip.Status.COMPLETED)

    def for_date(self, selected_date):
        return self.filter(trip_date=selected_date)


class TripManager(models.Manager.from_queryset(TripQuerySet)):
    pass


class Trip(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активна'
        CANCELLED = 'cancelled', 'Отменена'
        COMPLETED = 'completed', 'Завершена'

    route = models.ForeignKey('routes_app.Route', on_delete=models.PROTECT, related_name='trips', verbose_name='Маршрут')
    passenger = models.ForeignKey('users_app.Passenger', on_delete=models.PROTECT, related_name='trips', verbose_name='Пассажир')
    origin_stop = models.ForeignKey('stops_app.Stop', on_delete=models.PROTECT, related_name='departures', verbose_name='Остановка отправления')
    destination_stop = models.ForeignKey('stops_app.Stop', on_delete=models.PROTECT, related_name='arrivals', verbose_name='Остановка прибытия')
    trip_date = models.DateField('Дата поездки', db_index=True)
    status = models.CharField('Статус', max_length=12, choices=Status.choices, default=Status.ACTIVE, db_index=True)

    objects = TripManager()

    class Meta:
        db_table = 'trips'
        ordering = ('-trip_date', '-pk')
        verbose_name = 'поездка'
        verbose_name_plural = 'Поездки'
        indexes = [models.Index(fields=('route', 'trip_date', 'status'), name='trip_route_date_status_idx')]

    @property
    def number(self):
        return self.route.number

    @property
    def user_id(self):
        return self.passenger_id

    @property
    def stop_from_id(self):
        return self.origin_stop_id

    @property
    def stop_to_id(self):
        return self.destination_stop_id

    @property
    def has_benefits(self):
        return self.passenger.has_benefits

    @property
    def is_cancelled(self):
        return self.status == self.Status.CANCELLED

    @property
    def price(self):
        return round(float(self.route.base_price) * self.passenger.get_discount(), 2)

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save(update_fields=('status',))

    def __str__(self):
        return f'{self.route.number}: {self.passenger.name} ({self.trip_date})'
