from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Создаёт тестовые категории и продукты в базе данных'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем создание тестовых данных...')

        # 1. Создаём категории (если их ещё нет)
        categories_data = [
            {'name': 'Электроника'},
            {'name': 'Бытовая техника'},
            {'name': 'Гаджеты'},
            {'name': 'Компьютеры и комплектующие'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(name=cat_data['name'])
            if created:
                self.stdout.write(f'Создана категория: {category.name}')
            else:
                self.stdout.write(f'Категория уже существует: {category.name}')

        # 2. Создаём тестовые продукты
        products_data = [
            {
                'name': 'Ноутбук ASUS VivoBook',
                'price': 59999,
                'category_name': 'Электроника'
            },
            {
                'name': 'Телевизор Samsung 55"',
                'price': 49999,
                'category_name': 'Электроника'
            },
            {
                'name': 'Робот‑пылесос Xiaomi',
                'price': 19999,
                'category_name': 'Бытовая техника'
            },
            {
                'name': 'Стиральная машина LG',
                'price': 34999,
                'category_name': 'Бытовая техника'
            },
            {
                'name': 'Умные часы Apple Watch',
                'price': 29999,
                'category_name': 'Гаджеты'
            },
            {
                'name': 'Беспроводные наушники Sony',
                'price': 12999,
                'category_name': 'Гаджеты'
            },
            {
                'name': 'Видеокарта NVIDIA RTX 4080',
                'price': 129999,
                'category_name': 'Компьютеры и комплектующие'
            },
        ]

        created_count = 0
        for prod_data in products_data:
            try:
                category = Category.objects.get(name=prod_data['category_name'])
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    price=prod_data['price'],
                    category=category
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Создан продукт: {product.name} ({product.category.name}) — {product.price} руб.')
                    )
                else:
                    self.stdout.write(
                        f'Продукт уже существует: {product.name}'
                    )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Категория не найдена: {prod_data["category_name"]}')
                )

        self.stdout.write(self.style.SUCCESS(f'Готово! Создано {created_count} новых продуктов.'))