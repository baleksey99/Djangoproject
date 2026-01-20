from .models import Product
from django.core.cache import cache


def get_products_by_category(category_id, cache_timeout=60 * 15):
    """
    Возвращает продукты указанной категории с кешированием.


    """
    cache_key = f'category_products_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category').order_by('name')
        cache.set(cache_key, products, cache_timeout)

    return products
