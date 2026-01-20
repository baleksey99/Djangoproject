
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product  # Укажите путь к вашей модели Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        # Получаем контент‑тип для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Находим кастомное разрешение
        unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type,
        )
        # Находим стандартное разрешение на удаление
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Создаём группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Назначаем разрешения
        group.permissions.add(unpublish_perm, delete_perm)
        self.stdout.write(
            self.style.SUCCESS(
                'Права "can_unpublish_product" и "delete_product" назначены группе'
            )
        )
