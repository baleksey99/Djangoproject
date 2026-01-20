from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(_('Название'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

class Product(models.Model):
    name = models.CharField(_('Наименование'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)
    image = models.ImageField(
        _('Изображение'),
        upload_to='products/',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('Категория')
    )
    price = models.DecimalField(
        _('Цена за покупку'),
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(
        _('Дата последнего изменения'),
        auto_now=True
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Опубликован')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Владелец'),
        null=True,
        blank=True
    )
    # НОВОЕ ПОЛЕ: счётчик просмотров
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Количество просмотров')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]
