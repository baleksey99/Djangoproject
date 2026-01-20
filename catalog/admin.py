from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке продуктов
    list_display = ('id', 'name', 'price', 'category', 'is_published')
    list_filter = ('category', 'is_published')  # Фильтр по статусу публикации
    search_fields = ('name', 'description')

    # Поля, доступные для редактирования в админке
    fields = ('name', 'description', 'price', 'category', 'image', 'is_published')

    def has_delete_permission(self, request, obj=None):
        """
        Проверяет, есть ли у пользователя право удалять продукты.
        """
        return request.user.has_perm('catalog.delete_product')

    def has_change_permission(self, request, obj=None):
        """
        Проверяет, есть ли у пользователя право редактировать продукты.

        """

        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        """
        Делает поле `is_published` доступным только для модераторов.
        Для остальных — поле будет readonly (только для просмотра).
        """
        if request.user.has_perm('catalog.can_unpublish_product'):
            return []  # Все поля редактируемы
        else:
            return ['is_published']  # Только `is_published` — readonly

    def save_model(self, request, obj, form, change):
        """
        При сохранении проверяет, может ли пользователь изменить статус публикации.
        """
        if 'is_published' in form.changed_data:
            if not request.user.has_perm('catalog.can_unpublish_product'):
                # Если пользователь не модератор — запрещаем менять статус
                obj.is_published = form.initial.get('is_published', obj.is_published)
        super().save_model(request, obj, form, change)
