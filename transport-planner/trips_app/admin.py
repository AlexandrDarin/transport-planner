from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip_date', 'route', 'passenger', 'origin_stop', 'destination_stop', 'status', 'price_display')
    list_display_links = ('id', 'route')
    search_fields = ('route__number', 'passenger__name', 'origin_stop__name', 'destination_stop__name')
    list_filter = ('status', 'trip_date', 'route__transport_type')
    ordering = ('-trip_date', '-pk')
    list_select_related = ('route', 'passenger', 'origin_stop', 'destination_stop')
    date_hierarchy = 'trip_date'
    list_per_page = 30
    autocomplete_fields = ('route', 'passenger', 'origin_stop', 'destination_stop')

    @admin.display(description='Стоимость')
    def price_display(self, obj):
        return obj.price
