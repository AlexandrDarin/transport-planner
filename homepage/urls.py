from django.urls import path
from . import views
app_name = "homepage"
urlpatterns = [path("", views.index, name="index"), path("about/", views.about, name="about"), path("statistics/", views.statistics, name="statistics")]
