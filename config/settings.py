
import os
from dotenv import load_dotenv
from pathlib import Path
from decouple import config

# Загрузка переменных окружения из .env
load_dotenv(override=True)

# Основные пути
BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Хосты (разрешённые домены)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # Добавьте ваш домен в продакшене: 'ваш-сайт.ru'
]

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Ваши приложения
    'catalog',
    'blog',
    'users',
    # Дополнительные библиотеки
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',
    'django_extensions',
]

# Настройки Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# База данных (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Локализация
LANGUAGE_CODE = 'ru'  # Для русскоязычного сайта
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True  # Локализация форматов чисел/дат
USE_TZ = True

# Статические файлы (CSS, JavaScript, изображения)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Папка для разработки
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для продакшена (collectstatic)

# Медиафайлы (загрузки пользователей)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Логирование (опционально)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

AUTH_USER_MODEL = 'users.CustomUser'


LOGIN_URL = '/login/'  # URL для перенаправления неавторизованных
LOGIN_REDIRECT_URL = '/'  # Куда перенаправлять после входа




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'        # сервер Яндекс Почты
EMAIL_PORT = 465                      # порт для SSL
EMAIL_USE_TLS = False                 # для порта 465 используем SSL, а не TLS
EMAIL_USE_SSL = True                  # включаем SSL (обязательно для порта 465)
EMAIL_HOST_USER = os.getenv('EMAIL_USER')         # ваш email (например, user@yandex.ru)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD') # пароль или пароль приложения
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_USER')   # адрес «от кого»

EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')