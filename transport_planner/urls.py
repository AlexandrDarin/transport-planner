"""Маршрутизация верхнего уровня проекта transport_planner."""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path


admin.site.site_header = "Transport Planner — администрирование"
admin.site.site_title = "Transport Planner"
admin.site.index_title = "Управление данными сервиса"

urlpatterns = [
    *([path('__debug__/', include('debug_toolbar.urls'))] if settings.DEBUG_TOOLBAR_AVAILABLE else []),
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('routes/', include('routes_app.urls', namespace='routes')),
    path('trips/', include('trips_app.urls', namespace='trips')),
    path('users/', include('users_app.urls', namespace='users')),
    path('stops/', include('stops_app.urls', namespace='stops')),
]
