from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def is_product_moderator(user):
    """Проверяет, является ли пользователь модератором продуктов"""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name="Модератор продуктов").exists()


@register.filter
def can_unpublish_product(user):
    """Проверяет, может ли пользователь снимать продукты с публикации"""
    if not user.is_authenticated:
        return False
    return user.has_perm("fly.can_unpublish_product")


@register.filter
def can_change_publication_status(user):
    """Проверяет, может ли пользователь изменять статус публикации"""
    if not user.is_authenticated:
        return False
    return (
        user.has_perm("fly.can_change_publication_status")
        or user.groups.filter(name="Модератор продуктов").exists()
    )


@register.filter
def can_delete_any_product(user):
    """Проверяет, может ли пользователь удалять любые продукты"""
    if not user.is_authenticated:
        return False
    return (
        user.has_perm("fly.delete_product")
        or user.groups.filter(name="Модератор продуктов").exists()
    )
