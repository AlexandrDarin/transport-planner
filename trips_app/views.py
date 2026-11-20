"""Представления списка, создания, редактирования и отмены поездок."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import TripFilterForm, TripForm
from .models import Trip


def _with_price(queryset):
    return queryset.select_related(
        "route", "passenger", "origin_stop", "destination_stop"
    ).annotate(
        route_number=F("route__number"),
        transport_type=F("route__transport_type"),
        base_price=F("route__base_price"),
        passenger_name=F("passenger__name"),
        origin=F("origin_stop__name"),
        destination=F("destination_stop__name"),
    )


def trips_list(request):
    """Выводит поездки с проверенной GET-формой, сортировкой и пагинацией."""
    filter_data = request.GET if request.GET else {"status": "all", "sort": "date"}
    form = TripFilterForm(filter_data)
    form_is_valid = form.is_valid()
    filters = form.cleaned_data if form_is_valid else {}

    status = filters.get("status") or "all"
    query = (filters.get("q") or "").strip()
    selected_date = filters.get("date")
    sort = filters.get("sort") or "date"

    trips = Trip.objects.all()
    if status != "all":
        trips = trips.filter(status=status)
    if query:
        trips = trips.filter(
            Q(route__number__icontains=query)
            | Q(passenger__name__icontains=query)
            | Q(origin_stop__name__icontains=query)
            | Q(destination_stop__name__icontains=query)
        )
    if selected_date:
        trips = trips.filter(trip_date=selected_date)

    sort_map = {
        "date": "-trip_date",
        "date_asc": "trip_date",
        "route": "route__number",
        "passenger": "passenger__name",
    }
    trips = _with_price(trips.order_by(sort_map[sort], "-pk"))
    counts = Trip.objects.aggregate(
        total=Count("pk"),
        active=Count("pk", filter=Q(status=Trip.Status.ACTIVE)),
        cancelled=Count("pk", filter=Q(status=Trip.Status.CANCELLED)),
        completed=Count("pk", filter=Q(status=Trip.Status.COMPLETED)),
    )
    page_obj = Paginator(trips, 10).get_page(request.GET.get("page"))
    return render(request, "trips_app/list.html", {
        "trips": page_obj.object_list,
        "page_obj": page_obj,
        "stats": counts,
        "status": status,
        "query": query,
        "selected_date": selected_date.isoformat() if selected_date else "",
        "sort": sort,
        "form": form,
    })


def trip_detail(request, trip_id):
    """Показывает поездку или возвращает стандартный ответ 404."""
    trip = get_object_or_404(_with_price(Trip.objects.all()), pk=trip_id)
    return render(request, "trips_app/detail.html", {"trip": trip})


def trip_create(request):
    """Создаёт поездку только после валидации и проверки доступности маршрута."""
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            route = form.cleaned_data["route"]
            trip_date = form.cleaned_data["trip_date"]
            route_is_busy = Trip.objects.active().filter(
                route=route,
                trip_date=trip_date,
            ).exists()
            if route_is_busy:
                form.add_error(
                    None,
                    "На выбранную дату уже существует активная поездка по этому маршруту.",
                )
            else:
                form.save()
                messages.success(request, "Поездка успешно создана.")
                return redirect("trips:list")
    else:
        form = TripForm(initial={"trip_date": timezone.localdate()})

    return render(request, "trips_app/trip_form.html", {
        "form": form,
        "trip": None,
    })


def trip_update(request, trip_id):
    """Редактирует активную поездку через ModelForm(instance=trip)."""
    trip = get_object_or_404(Trip.objects.active(), pk=trip_id)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            route = form.cleaned_data["route"]
            trip_date = form.cleaned_data["trip_date"]
            route_is_busy = Trip.objects.active().filter(
                route=route,
                trip_date=trip_date,
            ).exclude(pk=trip.pk).exists()
            if route_is_busy:
                form.add_error(
                    None,
                    "На выбранную дату уже существует другая активная поездка по этому маршруту.",
                )
            else:
                form.save()
                messages.success(request, "Изменения поездки сохранены.")
                return redirect("trips:detail", trip_id=trip.pk)
    else:
        form = TripForm(instance=trip)

    return render(request, "trips_app/trip_form.html", {
        "form": form,
        "trip": trip,
    })


@require_POST
def trip_cancel(request, trip_id):
    """Отменяет поездку POST-запросом без физического удаления записи."""
    trip = get_object_or_404(Trip.objects.active(), pk=trip_id)
    trip.cancel()
    messages.success(request, "Поездка отменена. Запись сохранена в истории.")
    return redirect("trips:list")
