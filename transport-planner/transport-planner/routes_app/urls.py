"""Маршруты приложения routes_app."""

from django.urls import path

from . import views

app_name = "routes"

urlpatterns = [
    path("create/", views.route_create, name="create"),
    path("<int:route_id>/edit/", views.route_update, name="update"),
    path("", views.routes_list, name="list"),
    path("available/", views.available_routes, name="available"),
    path("slug/<slug:slug>/", views.route_detail_by_slug, name="slug-detail"),
    path("<int:route_id>/", views.route_detail, name="detail"),
]
