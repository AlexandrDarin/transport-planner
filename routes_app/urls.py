"""Маршруты приложения routes_app."""

from django.urls import path

from . import views

app_name = "routes"

urlpatterns = [
    path("", views.routes_list, name="list"),
    path("available/", views.available_routes, name="available"),
    path("<int:route_id>/", views.route_detail, name="detail"),
]
