from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='users:login')  # ← Защита: только для авторизованных
def product_create(request):
    """Создание товара."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно создан!')
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/create.html', {'form': form})

@login_required(login_url='users:login')  # ← Защита: только для авторизованных
def product_update(request, pk):
    """Редактирование товара."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт обновлён!')
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/update.html', {'form': form, 'product': product})

@login_required(login_url='users:login')  # ← Защита: только для авторизованных
def product_delete(request, pk):
    """Удаление товара."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Продукт удалён!')
        return redirect('catalog:product_list')
    return render(request, 'catalog/delete.html', {'product': product})
