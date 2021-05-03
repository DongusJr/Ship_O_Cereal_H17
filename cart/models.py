from django.db import models
from django.contrib.postgres.fields import ArrayField
from products.models import Products

# Create your models here.

class Cart(models.Model):
    product_list = ArrayField()
    total = models.IntegerField()

    @staticmethod
    def add_to_cart(product, user_id, quantity=1):
        cart = Cart.objects.get(id=user_id)
        if quantity>product.in_stock:
            return False
        cart.product_list.append({'quantity':quantity, 'product':product})
        Products.update_stock(product, quantity)
        return Cart.update_total(cart)

    @staticmethod
    def update_total(cart_object, total=0):
        cart_list = cart_object.product_list
        for item in cart_list:
            total += item['quantity']*(item['product'].price)
        cart_object.total = total

    @staticmethod
    def remove_item(item, user_id):
        cart = Cart.objects.get(id=user_id)
        cart.product_list.remove(item)
        Products.update_stock(item['product'], item['quantity'], 0)
        return Cart.update_total(cart)

