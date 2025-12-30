from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),           # Главная страница
    path('contacts/', views.contacts, name='contacts'),  # Страница контактов
    path('catalog/', include('catalog.urls')),    # URL приложения catalog
    path('admin/', admin.site.urls),            # Админка
]

# Обработка статических файлов (только для DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])