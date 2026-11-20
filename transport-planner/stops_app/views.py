from django.db.models import Q, Count
from django.shortcuts import render
from .models import Stop


def stops_list(request):
    query = request.GET.get('q', '').strip()[:100]
    stops = Stop.objects.annotate(departure_count=Count('departures'), arrival_count=Count('arrivals'))
    if query:
        stops = stops.filter(Q(name__icontains=query) | Q(city__icontains=query))
    return render(request, 'stops_app/list.html', {'stops': stops.order_by('city', 'name'), 'query': query})


def stop_detail(request, stop_id):
    stop = Stop.objects.filter(pk=stop_id).first()
    trips = stop.departures.select_related('route', 'passenger', 'destination_stop').order_by('trip_date') if stop else []
    arrivals = stop.arrivals.select_related('route', 'passenger', 'origin_stop').order_by('trip_date') if stop else []
    return render(request, 'stops_app/detail.html', {'stop': stop, 'trips': trips, 'arrivals': arrivals}, status=404 if stop is None else 200)
