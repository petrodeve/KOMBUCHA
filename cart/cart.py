from decimal import Decimal

from catalog.models import Product
from django.shortcuts import get_object_or_404


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id  in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def update_quantity(self, product, quantity):
        if quantity <= 0:
            self.remove(product)
        else:
            self.add(product, quantity, override_quantity=True)

    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        length = sum(item.quantity for item in self.cart.values())
        return length

    def get_total_price(self):
        total = sum(Decimal(item['price'] * item['quantity']) for item in self.cart.values())

        return total


    def get_cart_items(self):
        items = []
        for item in self:
            items.append({
                'product': item['product'],
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item['total_price']
            })

        return items