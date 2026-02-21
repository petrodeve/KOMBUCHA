from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from .models import Product,ProductImage
from django.db.models import Q


class CatalogView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_describe.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_desc'] = self.object
        return context
