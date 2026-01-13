from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации пользователя через email."""
    email = forms.EmailField(
        required=True,
        help_text='Обязательное поле. Укажите корректный email.'
    )

    class Meta:
        model = CustomUser
        fields = ('email',)  # Только email, т.к. username отключён
        field_classes = {'email': forms.EmailField}



class EmailAuthenticationForm(AuthenticationForm):
    """Форма для входа пользователя по email (вместо username)."""
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
