from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category

@cache_page(60 * 15)  # Кеш на 15 минут для HTTP-ответа
def product_list(request):
    """Страница списка товаров."""

    cache_key = 'published_products_v2'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(is_published=True)\
            .select_related('category')\
            .only('id', 'name', 'price', 'category__name')
        cache.set(cache_key, products, 60 * 15)

    return render(request, 'catalog/list.html', {'products': products})

@cache_page(60 * 15)
def product_detail(request, pk):
    """Страница детализации товара (доступна всем)."""
    product = get_object_or_404(Product, pk=pk)

    # Увеличиваем счётчик просмотров (не кешируется!)
    product.views_count += 1
    product.save(update_fields=['views_count'])

    return render(request, 'catalog/product_detail.html', {'product': product})

@login_required(login_url='users:login')
def product_create(request):
    """Создание товара (только для авторизованных)."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, 'Продукт успешно создан!')

            # Очищаем кеш списка товаров
            cache.delete('published_products')

            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/create.html', {'form': form})

@login_required(login_url='users:login')
def product_update(request, pk):
    """Редактирование товара (только владелец или модератор)."""
    product = get_object_or_404(Product, pk=pk)

    if not (product.owner == request.user or request.user.has_perm('catalog.can_unpublish_product')):
        messages.error(request, 'У вас нет прав на редактирование этого продукта.')
        return redirect('catalog:product_detail', pk=product.pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт обновлён!')

            # Очищаем кеш списка и детальной страницы
            cache.delete('published_products')
            cache.delete(f'product_{pk}')

            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/update.html', {'form': form, 'product': product})

@login_required(login_url='users:login')
def product_delete(request, pk):
    """Удаление товара (владелец или пользователь с правом delete_product)."""
    product = get_object_or_404(Product, pk=pk)

    if not (product.owner == request.user or request.user.has_perm('catalog.delete_product')):
        messages.error(request, 'У вас нет прав на удаление этого продукта.')
        return redirect('catalog:product_detail', pk=product.pk)


    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Продукт удалён!')

        # Очищаем кеш
        cache.delete('published_products')
        cache.delete(f'product_{pk}')


        return redirect('catalog:product_list')

    return render(request, 'catalog/delete.html', {'product': product})

@login_required(login_url='users:login')
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    """Снятие продукта с публикации (только для пользователей с правом can_unpublish_product)."""
    product = get_object_or_404(Product, pk=pk)

    if not product.is_published:
        messages.warning(request, 'Продукт уже снят с публикации.')
        return redirect('catalog:product_detail', pk=product.pk)

    product.is_published = False
    product.save()

    messages.success(request, f'Продукт "{product.name}" успешно снят с публикации.')


    # Очищаем кеш списка (товар больше не публикуется)
    cache.delete('published_products')

    return redirect('catalog:product_detail', pk=product.pk)

def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(
        category_id=category_id,
        is_published=True
    ).select_related('category')
    return render(request, 'catalog/category_products.html', {
        'category': category,
        'products': products
    })
