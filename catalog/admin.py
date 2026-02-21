from django.contrib import admin
from .models import Product, ProductImage



class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' ,'flavor', 'price', 'stock')
    list_filter = ('name','flavor')
    search_fields = ('name','flavor','description')
    prepopulated_fields = {'slug':('name', 'flavor')}
    inlines = (ProductImageInLine,)
# Register your models here.
admin.site.register(Product, ProductAdmin)