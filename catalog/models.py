from django.db import models

class Category(models.Model):
    name = models.CharField('Наименование', max_length=255, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']  # Сортировка по имени категории

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Наименование', max_length=255)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField('Цена за покупку', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['id']  # Сортировка по ID продукта

    def __str__(self):
        return self.name