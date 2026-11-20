"""Регрессионные тесты форм и сценариев ПР11 для приложения поездок."""

from datetime import timedelta
import io
import importlib.util
import tempfile
from unittest import skipUnless

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from routes_app.forms import RouteForm
from routes_app.models import Route
from stops_app.models import Stop
from users_app.models import Passenger

from .forms import TripFilterForm, TripForm
from .models import Trip


class TripFormsTests(TestCase):
    def setUp(self):
        self.route = Route.objects.create(
            number="ТЕСТ-11",
            transport_type="Автобус",
            base_price="100.00",
            travel_time_minutes=35,
        )
        self.other_route = Route.objects.create(
            number="ТЕСТ-12",
            transport_type="Трамвай",
            base_price="50.00",
            travel_time_minutes=20,
        )
        self.passenger = Passenger.objects.create(
            name="Тестовый пассажир",
            age=25,
            has_benefits=False,
        )
        self.origin = Stop.objects.create(name="Начальная", city="Москва")
        self.destination = Stop.objects.create(name="Конечная", city="Москва")

    def valid_trip_data(self, **overrides):
        data = {
            "route": self.route.pk,
            "passenger": self.passenger.pk,
            "origin_stop": self.origin.pk,
            "destination_stop": self.destination.pk,
            "trip_date": (timezone.localdate() + timedelta(days=2)).isoformat(),
        }
        data.update(overrides)
        return data

    def test_trip_filter_form_validates_get_parameters(self):
        form = TripFilterForm({
            "q": "ТЕСТ",
            "date": (timezone.localdate() + timedelta(days=2)).isoformat(),
            "status": Trip.Status.ACTIVE,
            "sort": "route",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["sort"], "route")

    def test_trip_filter_form_rejects_unknown_status_and_sort(self):
        form = TripFilterForm({"status": "unknown", "sort": "password"})
        self.assertFalse(form.is_valid())

    def test_trip_form_rejects_past_date(self):
        form = TripForm(self.valid_trip_data(
            trip_date=(timezone.localdate() - timedelta(days=1)).isoformat()
        ))
        self.assertFalse(form.is_valid())
        self.assertIn("trip_date", form.errors)

    def test_trip_form_rejects_same_origin_and_destination(self):
        form = TripForm(self.valid_trip_data(destination_stop=self.origin.pk))
        self.assertFalse(form.is_valid())
        self.assertIn("destination_stop", form.errors)

    def test_trip_create_saves_only_valid_data(self):
        response = self.client.post(
            reverse("trips:create"), self.valid_trip_data()
        )
        self.assertRedirects(response, reverse("trips:list"))
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(Trip.objects.get().status, Trip.Status.ACTIVE)

    def test_trip_create_rejects_busy_route(self):
        trip_date = timezone.localdate() + timedelta(days=2)
        Trip.objects.create(
            route=self.route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=trip_date,
        )
        response = self.client.post(
            reverse("trips:create"),
            self.valid_trip_data(trip_date=trip_date.isoformat()),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "уже существует активная поездка")
        self.assertEqual(Trip.objects.count(), 1)

    def test_cancel_requires_post_and_keeps_database_record(self):
        trip = Trip.objects.create(
            route=self.route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=timezone.localdate() + timedelta(days=2),
        )
        url = reverse("trips:cancel", args=[trip.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url)
        self.assertRedirects(response, reverse("trips:list"))
        trip.refresh_from_db()
        self.assertEqual(trip.status, Trip.Status.CANCELLED)
        self.assertEqual(Trip.objects.count(), 1)

    def test_trip_update_uses_existing_instance_without_duplicate(self):
        trip = Trip.objects.create(
            route=self.route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=timezone.localdate() + timedelta(days=2),
        )
        response = self.client.get(reverse("trips:update", args=[trip.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("trips:update", args=[trip.pk]),
            self.valid_trip_data(trip_date=trip.trip_date.isoformat()),
        )
        self.assertRedirects(response, reverse("trips:detail", args=[trip.pk]))
        self.assertEqual(Trip.objects.count(), 1)

    def test_trip_update_rejects_conflict_with_another_active_trip(self):
        trip_date = timezone.localdate() + timedelta(days=2)
        first = Trip.objects.create(
            route=self.route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=trip_date,
        )
        second = Trip.objects.create(
            route=self.other_route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=trip_date,
        )
        response = self.client.post(
            reverse("trips:update", args=[second.pk]),
            self.valid_trip_data(route=self.route.pk, trip_date=trip_date.isoformat()),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "другая активная поездка")
        second.refresh_from_db()
        self.assertEqual(second.route_id, self.other_route.pk)
        self.assertEqual(Trip.objects.count(), 2)
        self.assertEqual(first.status, Trip.Status.ACTIVE)

    def test_cancelled_trip_does_not_block_new_trip(self):
        trip_date = timezone.localdate() + timedelta(days=2)
        old_trip = Trip.objects.create(
            route=self.route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=trip_date,
            status=Trip.Status.CANCELLED,
        )
        response = self.client.post(
            reverse("trips:create"),
            self.valid_trip_data(trip_date=trip_date.isoformat()),
        )
        self.assertRedirects(response, reverse("trips:list"))
        self.assertEqual(Trip.objects.count(), 2)
        self.assertEqual(old_trip.status, Trip.Status.CANCELLED)

    def test_missing_or_cancelled_trip_cannot_be_edited(self):
        self.assertEqual(
            self.client.get(reverse("trips:update", args=[9999])).status_code,
            404,
        )
        trip = Trip.objects.create(
            route=self.route,
            passenger=self.passenger,
            origin_stop=self.origin,
            destination_stop=self.destination,
            trip_date=timezone.localdate() + timedelta(days=2),
            status=Trip.Status.CANCELLED,
        )
        self.assertEqual(
            self.client.get(reverse("trips:update", args=[trip.pk])).status_code,
            404,
        )


class RouteFormTests(TestCase):
    def test_route_form_has_explicit_fields_and_optional_image(self):
        form = RouteForm()
        self.assertEqual(
            set(form.fields),
            {"number", "transport_type", "base_price", "travel_time_minutes", "image"},
        )
        self.assertFalse(form.fields["image"].required)


    @skipUnless(importlib.util.find_spec("PIL"), "Для теста загрузки требуется Pillow.")
    def test_route_image_upload_is_saved_and_displayed(self):
        from PIL import Image

        image_buffer = io.BytesIO()
        Image.new("RGB", (2, 2), color=(40, 90, 160)).save(
            image_buffer, format="PNG"
        )
        png_bytes = image_buffer.getvalue()
        with tempfile.TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=media_dir):
                upload = SimpleUploadedFile(
                    "route.png", png_bytes, content_type="image/png"
                )
                response = self.client.post(
                    reverse("routes:create"),
                    {
                        "number": "ФОТО-11",
                        "transport_type": "Автобус",
                        "base_price": "80.00",
                        "travel_time_minutes": "30",
                        "image": upload,
                    },
                )
                self.assertEqual(response.status_code, 302)
                route = Route.objects.get(number="ФОТО-11")
                self.assertTrue(route.image)
                self.assertTrue(route.image.storage.exists(route.image.name))
                page = self.client.get(reverse("routes:detail", args=[route.pk]))
                self.assertContains(page, route.image.url)

    def test_route_create_and_update_pages_are_available(self):
        data = {
            "number": "ФОРМА-1",
            "transport_type": "Автобус",
            "base_price": "75.00",
            "travel_time_minutes": "25",
        }
        response = self.client.post(reverse("routes:create"), data)
        self.assertEqual(response.status_code, 302)
        route = Route.objects.get(number="ФОРМА-1")
        self.assertEqual(
            self.client.get(reverse("routes:update", args=[route.pk])).status_code,
            200,
        )
