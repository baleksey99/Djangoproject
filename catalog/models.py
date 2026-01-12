from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
