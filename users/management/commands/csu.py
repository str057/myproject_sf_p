from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()

        # Проверяем, существует ли пользователь
        if not User.objects.filter(email="admin@example.com").exists():
            user = User.objects.create_user(
                email="admin@example.com", password="123qwe"
            )
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан"))
        else:
            self.stdout.write(self.style.WARNING("Пользователь уже существует"))
