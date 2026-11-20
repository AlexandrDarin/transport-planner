from django.db import models


class Passenger(models.Model):
    name = models.CharField('ФИО пассажира', max_length=150)
    age = models.PositiveSmallIntegerField('Возраст')
    has_benefits = models.BooleanField('Есть льгота', default=False)

    class Meta:
        db_table = 'users'
        ordering = ('name',)
        verbose_name = 'пассажир'
        verbose_name_plural = 'Пассажиры'

    def get_discount(self):
        return 0.5 if self.has_benefits else 1.0

    def __str__(self):
        return self.name


