from django.urls import path
from catalog.views import CatalogView,ProductDetailView

app_name = 'catalog'
urlpatterns = [path('', CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),]