from django.contrib import admin
from .models import Category, Product, Parent


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")  #  Поиск по name и description


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")  #  требуемые поля
    list_filter = ("category",)  #  Фильтрация по категории
    search_fields = ("name", "description")  # Поиск по name и description

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    ###