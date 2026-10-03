"""Маршрутизация верхнего уровня проекта transport_planner."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('routes/', include('routes_app.urls')),
    path('trips/', include('trips_app.urls')),
    path('users/', include('users_app.urls')),
    path('stops/', include('stops_app.urls')),
]