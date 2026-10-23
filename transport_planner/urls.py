"""Маршрутизация верхнего уровня проекта transport_planner."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('routes/', include('routes_app.urls', namespace='routes')),
    path('trips/', include('trips_app.urls', namespace='trips')),
    path('users/', include('users_app.urls', namespace='users')),
    path('stops/', include('stops_app.urls', namespace='stops')),
]
