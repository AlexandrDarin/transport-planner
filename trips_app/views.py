from datetime import date
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import render
from .models import Trip


def _with_price(queryset):
    return queryset.select_related('route', 'passenger', 'origin_stop', 'destination_stop').annotate(
        route_number=F('route__number'), transport_type=F('route__transport_type'),
        base_price=F('route__base_price'), passenger_name=F('passenger__name'),
        origin=F('origin_stop__name'),
        destination=F('destination_stop__name'),
    )


def trips_list(request):
    status = request.GET.get('status', 'all')
    if status not in ('all', *Trip.Status.values):
        status = 'all'
    query = request.GET.get('q', '').strip()[:100]
    selected_date = request.GET.get('date', '').strip()
    trips = Trip.objects.all()
    if status != 'all':
        trips = trips.filter(status=status)
    if query:
        trips = trips.filter(Q(route__number__icontains=query) | Q(passenger__name__icontains=query) | Q(origin_stop__name__icontains=query) | Q(destination_stop__name__icontains=query))
    if selected_date:
        try:
            date.fromisoformat(selected_date)
            trips = trips.filter(trip_date=selected_date)
        except ValueError:
            selected_date = ''
    sort_map = {'date': '-trip_date', 'date_asc': 'trip_date', 'route': 'route__number', 'passenger': 'passenger__name'}
    sort = request.GET.get('sort', 'date')
    trips = _with_price(trips.order_by(sort_map.get(sort, '-trip_date'), '-pk'))
    counts = Trip.objects.aggregate(total=Count('pk'), active=Count('pk', filter=Q(status=Trip.Status.ACTIVE)), cancelled=Count('pk', filter=Q(status=Trip.Status.CANCELLED)), completed=Count('pk', filter=Q(status=Trip.Status.COMPLETED)))
    page_obj = Paginator(trips, 10).get_page(request.GET.get('page'))
    return render(request, 'trips_app/list.html', {'trips': page_obj.object_list, 'page_obj': page_obj, 'stats': counts, 'status': status, 'query': query, 'selected_date': selected_date, 'sort': sort})


def trip_detail(request, trip_id):
    trip = _with_price(Trip.objects.filter(pk=trip_id)).first()
    return render(request, 'trips_app/detail.html', {'trip': trip}, status=404 if trip is None else 200)
