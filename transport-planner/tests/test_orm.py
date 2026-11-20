import pytest
from django.urls import reverse
from django.test import Client
from routes_app.models import Route
from stops_app.models import Stop
from users_app.models import Passenger
from trips_app.models import Trip

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_graph():
    route = Route.objects.create(number='X-10', transport_type='Автобус', base_price=80, travel_time_minutes=25)
    start = Stop.objects.create(name='Начальная', city='Тестоград')
    finish = Stop.objects.create(name='Конечная', city='Тестоград')
    passenger = Passenger.objects.create(name='Тестовый пассажир', age=30, has_benefits=True)
    trip = Trip.objects.create(route=route, passenger=passenger, origin_stop=start, destination_stop=finish, trip_date='2030-01-01')
    return route, start, finish, passenger, trip


def test_relationships_and_reverse_relations(sample_graph):
    route, start, finish, passenger, trip = sample_graph
    assert trip.route == route
    assert trip.passenger == passenger
    assert trip.origin_stop == start
    assert route.trips.count() == 1
    assert passenger.trips.count() == 1
    assert start.departures.count() == 1
    assert finish.arrivals.count() == 1


def test_trip_queryset_statuses(sample_graph):
    trip = sample_graph[-1]
    assert Trip.objects.active().count() == 1
    trip.status = Trip.Status.CANCELLED
    trip.save()
    assert Trip.objects.active().count() == 0
    assert Trip.objects.cancelled().count() == 1


def test_route_search_filter_sort_and_aggregation(sample_graph):
    route = sample_graph[0]
    assert Route.objects.filter(number__icontains='x').get() == route
    assert Route.objects.exclude(base_price__lt=50).count() == 1
    assert Route.objects.order_by('-base_price').first() == route
    assert Route.objects.values('number').get()['number'] == 'X-10'


def test_web_pages_and_trip_filters(sample_graph):
    client = Client()
    assert client.get(reverse('routes:list'), {'q': 'X-10'}).status_code == 200
    assert client.get(reverse('trips:list'), {'status': 'active', 'page': '1'}).status_code == 200
    assert client.get(reverse('homepage:statistics')).status_code == 200
    assert client.get(reverse('trips:detail', args=[sample_graph[-1].pk])).status_code == 200


def test_admin_registers_domain_models():
    from django.contrib import admin
    assert Route in admin.site._registry
    assert Stop in admin.site._registry
    assert Passenger in admin.site._registry
    assert Trip in admin.site._registry


def test_completed_status_and_route_slug(sample_graph):
    route, _, _, _, trip = sample_graph
    trip.status = Trip.Status.COMPLETED
    trip.save(update_fields=('status',))
    assert Trip.objects.completed().get() == trip
    assert route.slug
    assert route.get_absolute_url() == reverse('routes:slug-detail', kwargs={'slug': route.slug})
    assert Client().get(route.get_absolute_url()).status_code == 200


def test_admin_changelists_open_for_staff(sample_graph):
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.create_superuser(
        username='admin-test', email='admin@example.test', password='test-pass-12345'
    )
    client = Client()
    client.force_login(user)
    for url in ('/admin/routes_app/route/', '/admin/stops_app/stop/',
                '/admin/users_app/passenger/', '/admin/trips_app/trip/'):
        assert client.get(url).status_code == 200


def test_context_processor_exposes_global_counts(sample_graph):
    response = Client().get(reverse('homepage:index'))
    assert response.context['routes_count'] == 1
    assert response.context['stops_count'] == 2
    assert response.context['active_trips_count'] == 1
