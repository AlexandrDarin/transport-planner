"""Маршруты приложения trips_app."""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.trips_list, name="trips"),
    path("<int:trip_id>/", views.trip_detail, name="trip_detail"),
]