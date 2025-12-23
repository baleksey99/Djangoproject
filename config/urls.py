
from django.urls import path
from . import views  # импорт из текущей директории (config/)

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]