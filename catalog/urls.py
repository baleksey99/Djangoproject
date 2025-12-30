from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import home

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # Главная страница
    # Другие ваши URL...
]

# Обработка статических файлов (только для DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])