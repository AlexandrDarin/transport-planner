from django.urls import path
from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.index, name="index"),
    path("routes/", views.routes_list, name="routes"),
    path("stops/", views.stops_list, name="stops"),
    path("trips/", views.trips_list, name="trips"),
    path("routes/available/", views.available_routes, name="available_routes"),
    path("statistics/", views.statistics, name="statistics"),
]
