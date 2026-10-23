"""Маршруты приложения stops_app."""

from django.urls import path

from . import views

app_name = "stops"

urlpatterns = [
    path("", views.stops_list, name="list"),
    path("<int:stop_id>/", views.stop_detail, name="detail"),
]
