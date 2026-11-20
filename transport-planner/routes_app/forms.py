"""Форма создания и редактирования маршрута с загрузкой изображения."""

from django import forms

from .models import Route


class RouteForm(forms.ModelForm):
    """ModelForm с ограничением размера загружаемого изображения."""

    class Meta:
        model = Route
        fields = (
            "number",
            "transport_type",
            "base_price",
            "travel_time_minutes",
            "image",
        )
        labels = {
            "number": "Номер маршрута",
            "transport_type": "Вид транспорта",
            "base_price": "Базовая стоимость, ₽",
            "travel_time_minutes": "Время в пути, мин",
            "image": "Изображение маршрута",
        }
        help_texts = {
            "image": "Необязательно. Формат изображения проверяется сервером, максимальный размер — 5 МБ.",
        }
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "transport_type": forms.TextInput(attrs={"class": "form-control"}),
            "base_price": forms.NumberInput(attrs={
                "class": "form-control", "min": "0", "step": "0.01",
            }),
            "travel_time_minutes": forms.NumberInput(attrs={
                "class": "form-control", "min": "1",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control", "accept": "image/*",
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and hasattr(image, "size") and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Размер изображения не должен превышать 5 МБ."
            )
        return image
