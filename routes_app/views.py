from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q
from datetime import date
<<<<<<< HEAD
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RouteForm
=======
from django.shortcuts import render
>>>>>>> 5474caf0f7714bfeba7f8bb98d28facb67b46cf3
from .models import Route
from trips_app.models import Trip


def routes_list(request):
    query = request.GET.get('q', '').strip()[:100]
    max_price = request.GET.get('max_price', '').strip()
    routes = Route.objects.all().annotate(trip_count=Count('trips'))
    if query:
        routes = routes.filter(Q(number__icontains=query) | Q(transport_type__icontains=query))
    if max_price:
        try:
            routes = routes.filter(base_price__lte=float(max_price))
        except (TypeError, ValueError):
            max_price = ''
    sort_map = {'number': 'number', '-number': '-number', 'price': 'base_price', '-price': '-base_price', 'duration': 'travel_time_minutes'}
    sort = request.GET.get('sort', 'number')
    routes = routes.order_by(sort_map.get(sort, 'number'), 'pk')
    stats = Route.objects.aggregate(count=Count('pk'), min_price=Min('base_price'), max_price=Max('base_price'), avg_price=Avg('base_price'))
    page_obj = Paginator(routes, 10).get_page(request.GET.get('page'))
    return render(request, 'routes_app/list.html', {'routes': page_obj.object_list, 'page_obj': page_obj, 'stats': stats, 'query': query, 'max_price': max_price, 'sort': sort})


def route_detail(request, route_id):
    route = Route.objects.annotate(trip_count=Count('trips')).filter(pk=route_id).first()
    trips = route.trips.select_related('passenger', 'origin_stop', 'destination_stop').order_by('trip_date', 'pk') if route else []
    return render(request, 'routes_app/detail.html', {'route': route, 'trips': trips}, status=404 if route is None else 200)


def available_routes(request):
    trip_date = request.GET.get('date', '').strip()
    routes = Route.objects.all()
    if trip_date:
        try:
            date.fromisoformat(trip_date)
        except ValueError:
            trip_date = ''
        else:
            busy_ids = Trip.objects.active().for_date(trip_date).values_list('route_id', flat=True)
            routes = routes.exclude(pk__in=busy_ids)
    return render(request, 'routes_app/available.html', {'routes': routes.order_by('number'), 'trip_date': trip_date})


def route_detail_by_slug(request, slug):
    """SEO-friendly URL маршрута по уникальному slug."""
    route = Route.objects.annotate(trip_count=Count('trips')).filter(slug=slug).first()
    trips = route.trips.select_related('passenger', 'origin_stop', 'destination_stop').order_by('trip_date', 'pk') if route else []
    return render(request, 'routes_app/detail.html', {'route': route, 'trips': trips}, status=404 if route is None else 200)
<<<<<<< HEAD


def route_create(request):
    """Создаёт маршрут и сохраняет загруженное изображение как медиафайл."""
    if request.method == "POST":
        form = RouteForm(request.POST, request.FILES)
        if form.is_valid():
            route = form.save()
            messages.success(request, "Маршрут успешно создан.")
            return redirect("routes:detail", route_id=route.pk)
    else:
        form = RouteForm()
    return render(request, "routes_app/route_form.html", {
        "form": form,
        "route": None,
    })


def route_update(request, route_id):
    """Редактирует маршрут, включая замену его изображения."""
    route = get_object_or_404(Route, pk=route_id)
    if request.method == "POST":
        form = RouteForm(request.POST, request.FILES, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения маршрута сохранены.")
            return redirect("routes:detail", route_id=route.pk)
    else:
        form = RouteForm(instance=route)
    return render(request, "routes_app/route_form.html", {
        "form": form,
        "route": route,
    })
=======
>>>>>>> 5474caf0f7714bfeba7f8bb98d28facb67b46cf3
