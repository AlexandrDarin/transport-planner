from django.db.models import Q, Count, Sum, F, Case, When, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.shortcuts import render
from .models import Passenger


def users_list(request):
    query = request.GET.get('q', '').strip()[:100]
    passengers = Passenger.objects.annotate(trip_count=Count('trips'))
    if query:
        passengers = passengers.filter(Q(name__icontains=query))
    return render(request, 'users_app/list.html', {'users': passengers.order_by('name'), 'query': query})


def user_detail(request, user_id):
    passenger = Passenger.objects.annotate(trip_count=Count('trips')).filter(pk=user_id).first()
    trips = passenger.trips.select_related('route', 'origin_stop', 'destination_stop').order_by('-trip_date') if passenger else []
    spent = passenger.trips.active().aggregate(total=Coalesce(Sum(ExpressionWrapper(F('route__base_price') * Case(When(passenger__has_benefits=True, then=Value(0.5)), default=Value(1.0)), output_field=FloatField())), Value(0.0))) if passenger else {'total': 0}
    return render(request, 'users_app/detail.html', {'user_item': passenger, 'trips': trips, 'spent': spent}, status=404 if passenger is None else 200)
