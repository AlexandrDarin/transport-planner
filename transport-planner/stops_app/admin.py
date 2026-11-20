from django.contrib import admin
from .models import Stop


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'departure_count', 'arrival_count')
    search_fields = ('name', 'city')
    list_filter = ('city',)
    ordering = ('city', 'name')
    list_per_page = 30

    @admin.display(description='Отправлений')
    def departure_count(self, obj):
        return obj.departures.count()

    @admin.display(description='Прибытий')
    def arrival_count(self, obj):
        return obj.arrivals.count()
