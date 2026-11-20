from django.db.models import Count, Sum, Avg, F, Q, Case, When, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.shortcuts import render
from routes_app.models import Route
from stops_app.models import Stop
from users_app.models import Passenger
from trips_app.models import Trip


def index(request):
    return render(request, 'homepage/index.html', {'stats': {'routes': Route.objects.count(), 'stops': Stop.objects.count(), 'trips': Trip.objects.count(), 'users': Passenger.objects.count()}})


def about(request):
    return render(request, 'homepage/about.html')


def statistics(request):
    try:
        min_trips = max(0, min(100000, int(request.GET.get('min_trips', '1'))))
    except (TypeError, ValueError):
        min_trips = 1
    summary = Trip.objects.aggregate(total_trips=Count('pk'), active_trips=Count('pk', filter=Q(status=Trip.Status.ACTIVE)), cancelled_trips=Count('pk', filter=Q(status=Trip.Status.CANCELLED)), completed_trips=Count('pk', filter=Q(status=Trip.Status.COMPLETED)))
    revenue = Trip.objects.active().aggregate(total=Coalesce(Sum(ExpressionWrapper(F('route__base_price') * Case(When(passenger__has_benefits=True, then=Value(0.5)), default=Value(1.0)), output_field=FloatField())), Value(0.0)))
    route_stats = Route.objects.annotate(trip_count=Count('trips', filter=Q(trips__status=Trip.Status.ACTIVE))).order_by('-trip_count', 'number')
    popular_routes = route_stats.filter(trip_count__gte=min_trips)
    type_stats = Route.objects.values('transport_type').annotate(routes_count=Count('pk'), avg_price=Avg('base_price')).order_by('-routes_count', 'transport_type')
    user_stats = Passenger.objects.annotate(trips_count=Count('trips', filter=Q(trips__status=Trip.Status.ACTIVE)), total_spent=Coalesce(Sum(ExpressionWrapper(F('trips__route__base_price') * Case(When(has_benefits=True, then=Value(0.5)), default=Value(1.0)), output_field=FloatField()), filter=Q(trips__status=Trip.Status.ACTIVE)), Value(0.0))).order_by('-total_spent', 'name')
    city_stats = Stop.objects.values('city').annotate(stops_count=Count('pk')).order_by('-stops_count', 'city')
    top_stops = Stop.objects.annotate(departure_count=Count('departures', filter=Q(departures__status=Trip.Status.ACTIVE))).order_by('-departure_count', 'name')[:3]
    return render(request, 'homepage/statistics.html', {'min_trips': min_trips, 'summary': summary, 'revenue': revenue, 'route_stats': route_stats, 'popular_routes': popular_routes, 'type_stats': type_stats, 'user_stats': user_stats, 'city_stats': city_stats, 'top_stops': top_stops})
