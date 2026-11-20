from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Route(models.Model):
    number = models.CharField('Номер маршрута', max_length=30, unique=True)
    transport_type = models.CharField('Вид транспорта', max_length=50)
    base_price = models.DecimalField('Базовая стоимость', max_digits=8, decimal_places=2)
    travel_time_minutes = models.PositiveIntegerField('Время в пути, мин')
    slug = models.SlugField('Адрес', max_length=100, unique=True, blank=True)
    image = models.ImageField(
        'Изображение', upload_to='routes/', blank=True, null=True
    )

    class Meta:
        db_table = 'routes'
        ordering = ('number',)
        verbose_name = 'маршрут'
        verbose_name_plural = 'Маршруты'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.number, allow_unicode=False) or f'route-{self.pk or "new"}'
            candidate = base
            suffix = 2
            while Route.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f'{base}-{suffix}'
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('routes:slug-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.number} — {self.transport_type}'
