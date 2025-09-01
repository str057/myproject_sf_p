import os
import django

# Установите настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Создаем суперпользователя
try:
    user = User.objects.create(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    user.set_password('Admin123!')  # Надежный пароль
    user.save()

    print('✅ Суперпользователь создан успешно!')
    print('📧 Логин: admin@example.com')
    print('🔑 Пароль: Admin123!')

except Exception as e:
    print(f'❌ Ошибка: {e}')