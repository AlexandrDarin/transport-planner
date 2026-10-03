"""Маршруты приложения stops_app."""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.stops_list, name="stops"),
    path("<int:stop_id>/", views.stop_detail, name="stop_detail"),
]