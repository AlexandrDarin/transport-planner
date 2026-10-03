"""Маршруты приложения users_app."""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.users_list, name="users"),
    path("<int:user_id>/", views.user_detail, name="user_detail"),
]