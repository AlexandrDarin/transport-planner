"""Формы поиска, создания и редактирования поездок."""

from django import forms
from django.utils import timezone

from routes_app.models import Route
from stops_app.models import Stop
from users_app.models import Passenger

from .models import Trip


class TripFilterForm(forms.Form):
    """Проверяет параметры GET-фильтрации списка поездок."""

    STATUS_CHOICES = [
        ("all", "Все статусы"),
        *Trip.Status.choices,
    ]
    SORT_CHOICES = [
        ("date", "Сначала новые"),
        ("date_asc", "Сначала старые"),
        ("route", "По маршруту"),
        ("passenger", "По пассажиру"),
    ]

    q = forms.CharField(
        required=False,
        max_length=100,
        label="Поиск",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Маршрут, пассажир или остановка",
        }),
    )
    date = forms.DateField(
        required=False,
        label="Дата поездки",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
        }),
    )
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        label="Статус",
        initial="all",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        label="Сортировка",
        initial="date",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class TripForm(forms.ModelForm):
    """ModelForm для создания и редактирования поездки."""

    class Meta:
        model = Trip
        fields = (
            "route",
            "passenger",
            "origin_stop",
            "destination_stop",
            "trip_date",
        )
        labels = {
            "route": "Маршрут",
            "passenger": "Пассажир",
            "origin_stop": "Остановка отправления",
            "destination_stop": "Остановка прибытия",
            "trip_date": "Дата поездки",
        }
        help_texts = {
            "route": "Выберите маршрут. На одну дату допускается одна активная поездка по маршруту.",
            "passenger": "Выберите пассажира из существующего списка.",
            "origin_stop": "Остановка, с которой начинается поездка.",
            "destination_stop": "Остановка, на которой заканчивается поездка.",
            "trip_date": "Сегодняшняя или будущая дата.",
        }
        widgets = {
            "route": forms.Select(attrs={"class": "form-select"}),
            "passenger": forms.Select(attrs={"class": "form-select"}),
            "origin_stop": forms.Select(attrs={"class": "form-select"}),
            "destination_stop": forms.Select(attrs={"class": "form-select"}),
            "trip_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["route"].queryset = Route.objects.order_by("number")
        self.fields["passenger"].queryset = Passenger.objects.order_by("name")
        self.fields["origin_stop"].queryset = Stop.objects.order_by("city", "name")
        self.fields["destination_stop"].queryset = Stop.objects.order_by(
            "city", "name"
        )

    def clean_trip_date(self):
        """Запрещает создание и перенос поездки на прошедшую дату."""
        trip_date = self.cleaned_data["trip_date"]
        if trip_date < timezone.localdate():
            raise forms.ValidationError(
                "Нельзя создать поездку на прошедшую дату."
            )
        return trip_date

    def clean(self):
        """Проверяет согласованность остановок поездки."""
        cleaned_data = super().clean()
        origin = cleaned_data.get("origin_stop")
        destination = cleaned_data.get("destination_stop")
        if origin and destination and origin == destination:
            self.add_error(
                "destination_stop",
                "Остановка прибытия должна отличаться от остановки отправления.",
            )
        return cleaned_data
