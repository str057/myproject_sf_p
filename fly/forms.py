from django import forms
from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError
from datetime import datetime
from fly.models import Product, Parent


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ProdForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("views_counter",)


class ParentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"

    def clean_year_born(self):
        year_born = self.cleaned_data['year_born']
        current_year = datetime.now().year
        age = current_year - year_born

        if age >= 180:
            raise ValidationError("Неверный год рождения - возраст слишком большой")
        if year_born > current_year:
            raise ValidationError("Год рождения не может быть в будущем")

        return year_born