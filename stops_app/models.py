from django.db import models


class Stop(models.Model):
    name = models.CharField('Название остановки', max_length=150)
    city = models.CharField('Город', max_length=100)

    class Meta:
        db_table = 'stops'
        ordering = ('city', 'name')
        verbose_name = 'остановка'
        verbose_name_plural = 'Остановки'
        constraints = [models.UniqueConstraint(fields=('name', 'city'), name='unique_stop_name_city')]

    def __str__(self):
        return f'{self.name}, {self.city}'
