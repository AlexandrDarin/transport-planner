"""Маршруты приложения trips_app."""

from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("", views.trips_list, name="list"),
    path("<int:trip_id>/", views.trip_detail, name="detail"),
]
