from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    flavor = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/catalog', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def stock_message(self):
        if self.stock == 0:
            return "Not available"
        if self.stock < 10:
            return f"Remaining {self.stock} pc."
        return "Available"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/image', blank=True)