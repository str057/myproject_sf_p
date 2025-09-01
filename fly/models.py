from email.policy import default

from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]  # Сортировка по имени

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "png"])],  # Только JPG/PNG
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True,
        blank=True,
        help_text="Необязательное поле",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],  # Цена >= 0
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]  # Новые продукты сначала

    def __str__(self):
        return f"{self.name} - {self.price if self.price else 'Цена не указана'}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/default-product.png"


class Parent(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="parents",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Продукт",
    )
    name = models.CharField(
        max_length=100, verbose_name="Наименование",help_text="Введите ")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию",
        null=True,
        blank=True,
        related_name="parents_product",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Введите цену",
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],  # Цена >= 0
    )

    class Meta:
        verbose_name = "Категория родитель"
        verbose_name_plural = "Категории родитель"
        ordering = ["name"]  # Сортировка по имени

    def __str__(self):
        return self.name