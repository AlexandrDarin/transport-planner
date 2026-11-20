from routes_app.models import Route
from stops_app.models import Stop
from trips_app.models import Trip


def site_context(request):
    """Общие данные навигации, доступные во всех шаблонах."""
    return {
        'site_name': 'Transport Planner',
        'routes_count': Route.objects.count(),
        'stops_count': Stop.objects.count(),
        'active_trips_count': Trip.objects.active().count(),
    }
