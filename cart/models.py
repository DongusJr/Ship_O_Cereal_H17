from django.db import models
from django.contrib.postgres.fields import ArrayField
from cart.models import Cart
from products.models import Products
from users.models import PreviousOrders, Order, OrderProduct

# Create your models here.

class Contains(models.Model):
    quantity = models.IntergerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Cart(models.Model):
    # Possibly have user id
    total = models.IntegerField()

    @staticmethod
    def add_to_cart(product, user_id, quantity=1):
        cart = Cart.objects.get(pk=user_id)
        #if quantity>product.in_stock:
        #    return False
        contains = Contains.objects.create(cart=cart, product=product, quantity=quantity)
        # cart.product_list.append({'quantity':quantity, 'product':product})
        #Products.update_stock(product, quantity)
        Cart.update_total(cart)
        return True

    @staticmethod
    def update_total(cart_object, total=0):
        contains_list = Contains.objects.get(cart=cart_object)
        for item in contains_list:
            total += item.quantity*(item.product.price)
        cart_object.total = total
        return True

    @staticmethod
    def remove_item(product, user_id):
        cart = Cart.objects.get(id=user_id)
        contains = Contains.objects.get(cart=cart, product=product)
        Products.update_stock(product, contains.quantity, state=0)
        del contains
        Cart.update_total(cart)
        return True

    @staticmethod
    def complete_cart(user_id):
        cart = Cart.objects.get(id=user_id)
        contains_of_cart = Contains.objects.get(cart=cart)
        prev_order = PreviousOrders.objects.get(id=user_id)
        order = Order.objects.create(prev=prev_order)
        for contain in contains_of_cart:
            OrderProduct.objects.create(quantity=contain.quantity, order=order, product=contain.product)
            del contain
        Cart.update_total(cart)
        prev_order = PreviousOrders.objects.get(id=user_id)
        return True

