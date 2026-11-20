"""Маршрутизация верхнего уровня проекта transport_planner."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import include, path


admin.site.site_header = "Transport Planner — администрирование"
admin.site.site_title = "Transport Planner"
admin.site.index_title = "Управление данными сервиса"

urlpatterns = [
<<<<<<< HEAD
    *(
        [path("__debug__/", include("debug_toolbar.urls"))]
        if settings.DEBUG_TOOLBAR_AVAILABLE
        else []
    ),
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("routes/", include("routes_app.urls", namespace="routes")),
    path("trips/", include("trips_app.urls", namespace="trips")),
    path("users/", include("users_app.urls", namespace="users")),
    path("stops/", include("stops_app.urls", namespace="stops")),
=======
    *([path('__debug__/', include('debug_toolbar.urls'))] if settings.DEBUG_TOOLBAR_AVAILABLE else []),
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('routes/', include('routes_app.urls', namespace='routes')),
    path('trips/', include('trips_app.urls', namespace='trips')),
    path('users/', include('users_app.urls', namespace='users')),
    path('stops/', include('stops_app.urls', namespace='stops')),
>>>>>>> 5474caf0f7714bfeba7f8bb98d28facb67b46cf3
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
