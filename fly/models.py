from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    class PublicationStatus(models.TextChoices):
        DRAFT = "draft", _("Черновик")
        PUBLISHED = "published", _("Опубликовано")
        REJECTED = "rejected", _("Отклонено")
        ARCHIVED = "archived", _("В архиве")

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="ВВедите описание продукта",
        blank=True,
        null=True,
    )
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

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    # ДОБАВЛЯЕМ ПОЛЕ СТАТУСА ПУБЛИКАЦИИ (ЗАДАНИЕ 1)
    publication_status = models.CharField(
        max_length=20,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        verbose_name="Статус публикации",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]
        permissions = [
            ("can_edit_breed", "Can edit breed"),
            ("can_edit_description", "Can edit description"),
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_publication_status", "Может изменять статус публикации"),
        ]

    def __str__(self):
        return f"{self.name} - {self.price if self.price else 'Цена не указана'}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/default-product.png"

    # Методы для проверки прав доступа
    def can_be_edited_by(self, user):
        """Может ли пользователь редактировать продукт"""
        return self.owner == user

    def can_be_deleted_by(self, user):
        """Может ли пользователь удалить продукт"""
        return (
            self.owner == user
            or user.has_perm("fly.delete_product")
            or user.groups.filter(name="Модератор продуктов").exists()
        )

    def can_change_publication_status(self, user):
        """Может ли пользователь изменять статус публикации"""
        return (
            self.owner == user
            or user.has_perm("fly.can_change_publication_status")
            or user.groups.filter(name="Модератор продуктов").exists()
        )


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
        max_length=100, verbose_name="Наименование", help_text="Введите "
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категориу",
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
