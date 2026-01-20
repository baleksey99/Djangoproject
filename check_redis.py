
import os
import django
from django.conf import settings
import redis


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Инициализируем Django
try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка инициализации Django: {e}")
    exit(1)

# 3. Проверяем настройки кэша
try:
    if 'redis' in settings.CACHES['default']['BACKEND']:
        print("✅ Django настроен на использование Redis как кэша")
    else:
        print("⚠️ Django не использует Redis как кэш")
except KeyError as e:
    print(f"❌ Ошибка: отсутствует настройка CACHES — {e}")

# 4. Проверяем прямое подключение к Redis
try:
    # Используем URL из настроек
    redis_url = settings.CACHES['default']['LOCATION']
    client = redis.from_url(redis_url)  # ← автоматически разбирает URL
    client.ping()
    print("✅ Прямое подключение к Redis: OK")
except Exception as e:
    print(f"❌ Ошибка подключения к Redis: {e}")
