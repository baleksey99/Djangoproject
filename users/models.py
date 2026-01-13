from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    # Отключаем username, делаем email обязательным и уникальным
    username = None
    email = models.EmailField('email address', unique=True)

    # Дополнительные поля
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        null=True,
        blank=True
    )
    country = models.CharField(max_length=100, null=True, blank=True)

    # Делаем email основным полем для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email уже обязателен, другие поля не требуются

    def __str__(self):
        return self.email
