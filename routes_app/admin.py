from django.contrib import admin
from .models import Route


class TripInline(admin.TabularInline):
    model = __import__('trips_app.models', fromlist=['Trip']).Trip
    extra = 0
    fields = ('trip_date', 'passenger', 'status')
    readonly_fields = ('trip_date', 'passenger', 'status')
    can_delete = False
    show_change_link = True


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('number', 'transport_type', 'base_price', 'travel_time_minutes', 'trip_count')
    list_display_links = ('number',)
    search_fields = ('number', 'transport_type')
    list_filter = ('transport_type',)
    ordering = ('number',)
    list_per_page = 25
    prepopulated_fields = {'slug': ('number',)}
    inlines = (TripInline,)

    @admin.display(description='Поездок')
    def trip_count(self, obj):
        return obj.trips.count()
