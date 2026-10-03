"""Маршруты приложения routes_app."""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.routes_list, name="routes"),
    path("<int:route_id>/", views.route_detail, name="route_detail"),
]