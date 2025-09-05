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
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProdForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product

        exclude = ("views_counter", "owner", "publication_status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].required = False


class FlyModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ("description", "publication_status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["publication_status"].choices = [
            ("published", "Опубликовано"),
            ("rejected", "Отклонено"),
            ("archived", "В архиве"),
        ]


class ProductStatusForm(StyleFormMixin, ModelForm):
    """Форма для изменения статуса продукта"""

    class Meta:
        model = Product
        fields = ("publication_status",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and user.groups.filter(name="Модератор продуктов").exists():

            self.fields["publication_status"].choices = (
                Product.PublicationStatus.choices
            )
        else:

            self.fields["publication_status"].choices = [
                ("draft", "Черновик"),
                ("published", "Опубликовано"),
            ]


class ParentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"

    def clean_year_born(self):
        year_born = self.cleaned_data["year_born"]
        current_year = datetime.now().year
        age = current_year - year_born

        if age >= 180:
            raise ValidationError("Неверный год рождения - возраст слишком большой")
        if year_born > current_year:
            raise ValidationError("Год рождения не может быть в будущем")

        return year_born


class ProductPublishForm(forms.Form):
    """Форма для быстрой публикации продукта"""

    confirm = forms.BooleanField(
        required=True,
        label="Подтвердите публикацию продукта",
        help_text="Продукт станет видимым для всех пользователей",
    )


class ProductUnpublishForm(forms.Form):
    """Форма для быстрого снятия с публикации"""

    confirm = forms.BooleanField(
        required=True,
        label="Подтвердите снятие с публикации",
        help_text="Продукт будет скрыт от пользователей",
    )
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Причина (необязательно)",
        help_text="Укажите причину снятия с публикации",
    )
