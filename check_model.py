import os
import django
from django.conf import settings

# Укажите путь к вашим настройкам
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализация Django
django.setup()

# Проверка INSTALLED_APPS
print("✅ INSTALLED_APPS:", settings.INSTALLED_APPS)

# Попытка импортировать модель
try:
    from users.models import CustomUser
    print("✅ Модель CustomUser успешно импортирована:", CustomUser)
    print("   Поля модели:", [field.name for field in CustomUser._meta.fields])
except Exception as e:
    print("❌ Ошибка при импорте CustomUser:", e)
