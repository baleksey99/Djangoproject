
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login

def register_view(request):
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

                pass

            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:

            return render(request, 'users/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
