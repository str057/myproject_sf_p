from django.contrib import admin
from .models import Category, Product, Parent


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
        "owner",
        "publication_status",
        "created_at",
    )
    list_filter = ("category", "publication_status", "owner")
    search_fields = ("name", "description", "owner__username")
    list_editable = ("publication_status",)
    readonly_fields = ("created_at", "updated_at", "views_counter")


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
