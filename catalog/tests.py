from django.test import TestCase
from catalog.models import Product, Category

class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Тест-категория")
        self.product = Product.objects.create(
            name="Тест-товар",
            price=100,
            description="Описание",
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Тест-товар")