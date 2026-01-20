from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login

def register_view(request):
    # Пример: кешируем вспомогательный список стран (если используется в форме)
    countries = cache.get('countries_list')
    if countries is None:
        # Допустим, здесь тяжёлый запрос или парсинг
        countries = ['Россия', 'США', 'Германия']  # Ваш источник данных
        cache.set('countries_list', countries, 60 * 60)  # 1 час

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            try:
                send_mail(
                    'Добро пожаловать!',
                    f'Здравствуйте, {user.email}! Спасибо за регистрацию.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Логирование ошибки (опционально)
                pass

            # Очищаем кеш, если он зависит от списка пользователей
            cache.delete('users_count')  # Например, если где-то отображается число пользователей

            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {
        'form': form,
        'countries': countries  # Передаём в шаблон (если нужно)
    })

def login_view(request):
    # Пример: кешируем сообщение о правилах входа (если оно статично)
    login_hint = cache.get('login_hint')
    if login_hint is None:
        login_hint = 'Введите email и пароль. Если забыли пароль — воспользуйтесь восстановлением.'
        cache.set('login_hint', login_hint, 60 * 30)  # 30 минут

    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'users/login.html', {
                'form': form,
                'login_hint': login_hint
            })
    else:
        form = EmailAuthenticationForm()

    return render(request, 'users/login.html', {
        'form': form,
        'login_hint': login_hint
    })
