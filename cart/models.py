from django.db import models
from django.contrib.postgres.fields import ArrayField
from cart.models import Cart
from products.models import Products
from users.models import PreviousOrder

# Create your models here.

class Cart(models.Model):
    product_list = ArrayField(models.ForeignKey(Products, on_delete=models.CASCADE))
    total = models.IntegerField()

    @staticmethod
    def add_to_cart(product, user_id, quantity=1):
        cart = Cart.objects.get(pk=user_id)
        #if quantity>product.in_stock:
        #    return False
        cart.product_list.append({'quantity':quantity, 'product':product})
        #Products.update_stock(product, quantity)
        Cart.update_total(cart)
        return True

    @staticmethod
    def update_total(cart_object, total=0):
        cart_list = cart_object.product_list
        for item in cart_list:
            total += item['quantity']*(item['product'].price)
        cart_object.total = total
        return True

    @staticmethod
    def remove_item(item, user_id):
        cart = Cart.objects.get(id=user_id)
        cart.product_list.remove(item)
        #Products.update_stock(item['product'], item['quantity'], 0)
        Cart.update_total(cart)
        return True

    @staticmethod
    def complete_cart(user_id):
        cart = Cart.objects.get(id=user_id)
        prev_ord = PreviousOrder.objects.get(id=user_id)
        prev_ord.create_order()
        cart.product_list = ArrayField()
        cart.total = 0
        return True

