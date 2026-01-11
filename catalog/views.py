from django.views.generic import DetailView, ListView, TemplateView
from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'  # имя параметра в URL


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()[:10]  # как в исходном FBV


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'