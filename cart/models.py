from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from products.models import Products
from users.models import Order, OrderProduct

# Create your models here.

class Cart(models.Model):
    # Possibly have user id
    total = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def add_to_cart(self, product, quantity=1):
        cart = Cart.objects.get_or_create(self.request.user)
        contains = Contains.objects.create(cart=cart, product=product, quantity=quantity)
        Cart.update_total(cart)
        return True

    @staticmethod
    def update_total(cart_object, total=0):
        contains_list = Contains.objects.get(cart=cart_object)
        for item in contains_list:
            total += item.quantity*(item.product.price)
        cart_object.total = total
        return True

    def remove_item(self, product):
        cart = Cart.objects.get(user=self.request.user)
        contains = Contains.objects.get(cart=cart, product=product)
        Products.update_stock(product, contains.quantity, state=0)
        del contains
        Cart.update_total(cart)
        return True

    def complete_cart(self, user_id):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            return
        contains_of_cart = Contains.objects.get(cart=cart)
        prev_order = self.request.user.order
        order = Order.objects.create(prev=prev_order)
        for contain in contains_of_cart:
            OrderProduct.objects.create(quantity=contain.quantity, order=order, product=contain.product)
            del contain
        Cart.update_total(cart)
        return True

class Contains(models.Model):
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

