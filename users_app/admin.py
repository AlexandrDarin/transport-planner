from django.contrib import admin
from .models import Passenger


class TripInline(admin.TabularInline):
    model = __import__('trips_app.models', fromlist=['Trip']).Trip
    fk_name = 'passenger'
    extra = 0
    fields = ('route', 'trip_date', 'status')
    readonly_fields = ('route', 'trip_date', 'status')
    can_delete = False
    show_change_link = True


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'has_benefits', 'trip_count')
    search_fields = ('name',)
    list_filter = ('has_benefits',)
    ordering = ('name',)
    list_editable = ('has_benefits',)
    list_per_page = 30
    inlines = (TripInline,)

    @admin.display(description='Поездок')
    def trip_count(self, obj):
        return obj.trips.count()
