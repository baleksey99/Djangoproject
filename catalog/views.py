from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def product_list(request):
    """Страница списка товаров (доступна всем)."""
    products = Product.objects.all().select_related('category')
    return render(request, 'catalog/list.html', {'products': products})

def product_detail(request, pk):
    """Страница детализации товара (доступна всем)."""
    product = get_object_or_404(Product, pk=pk)
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
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/update.html', {'form': form, 'product': product})


@login_required(login_url='users:login')
def product_delete(request, pk):
    """Удаление товара (владелец или пользователь с правом delete_product)."""
    product = get_object_or_404(Product, pk)


@login_required(login_url='users:login')
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    """Снятие продукта с публикации (только для пользователей с правом can_unpublish_product)."""
    product = get_object_or_404(Product, pk=pk)

    # Проверяем, что продукт уже опубликован (иначе нечего снимать)
    if not product.is_published:
        messages.warning(request, 'Продукт уже снят с публикации.')
        return redirect('catalog:product_detail', pk=product.pk)

    # Снимаем с публикации
    product.is_published = False
    product.save()

    messages.success(request, f'Продукт "{product.name}" успешно снят с публикации.')
    return redirect('catalog:product_detail', pk=product.pk)
