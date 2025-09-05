from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from fly.models import Product


class Command(BaseCommand):
    help = "Создает группы и назначает разрешения для модераторов продуктов"

    def handle(self, *args, **options):
        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем или создаем разрешения
        unpublish_permission, created = Permission.objects.get_or_create(
            codename="can_unpublish_product",
            name="Может отменять публикацию продукта",
            content_type=content_type,
        )

        change_status_permission, created = Permission.objects.get_or_create(
            codename="can_change_publication_status",
            name="Может изменять статус публикации",
            content_type=content_type,
        )

        # Получаем стандартные разрешения
        delete_permission = Permission.objects.get(
            codename="delete_product", content_type=content_type
        )
        change_permission = Permission.objects.get(
            codename="change_product", content_type=content_type
        )
        view_permission = Permission.objects.get(
            codename="view_product", content_type=content_type
        )

        # Создаем группу модераторов продуктов
        moderator_group, created = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        # Назначаем разрешения группе
        moderator_group.permissions.add(
            unpublish_permission,
            change_status_permission,
            delete_permission,
            change_permission,
            view_permission,
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана успешно')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )

        self.stdout.write(
            self.style.SUCCESS("Разрешения успешно назначены группе модераторов")
        )

        # Создаем группу для обычных пользователей (опционально)
        user_group, created = Group.objects.get_or_create(name="Обычные пользователи")

        # Обычным пользователям даем только право просмотра
        user_group.permissions.add(view_permission)

        self.stdout.write(
            self.style.SUCCESS("Группы и разрешения успешно созданы и настроены")
        )
