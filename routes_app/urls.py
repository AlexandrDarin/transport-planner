from django.urls import path
from . import views
app_name = "routes"
urlpatterns = [path("", views.routes_list, name="list"), path("<int:route_id>/", views.route_detail, name="detail")]
