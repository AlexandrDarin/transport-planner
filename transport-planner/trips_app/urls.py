"""Маршруты приложения trips_app."""

from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("create/", views.trip_create, name="create"),
    path("<int:trip_id>/edit/", views.trip_update, name="update"),
    path("<int:trip_id>/cancel/", views.trip_cancel, name="cancel"),
    path("", views.trips_list, name="list"),
    path("<int:trip_id>/", views.trip_detail, name="detail"),
]
