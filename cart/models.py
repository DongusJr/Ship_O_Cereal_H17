from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from products.models import Products
from users.models import Order

# Create your models here.

class Cart(models.Model):
    # Possibly have user id
    total = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @staticmethod
    def update_total(cart_object, total=0):
        contains_list = Contains.objects.filter(cart=cart_object)
        for item in contains_list:
            total += item.quantity*(item.product.price)
        cart_object.total = total
        return cart_object



    # def complete_cart(self, user_id):
    #     try:
    #         cart = Cart.objects.get(user=self.request.user)
    #     except:
    #         return
    #     contains_of_cart = Contains.objects.get(cart=cart)
    #     prev_order = self.request.user.order
    #     order = Order.objects.create(prev=prev_order)
    #     for contain in contains_of_cart:
    #         OrderProduct.objects.create(quantity=contain.quantity, order=order, product=contain.product)
    #         del contain
    #     Cart.update_total(cart)
    #     return True

class Contains(models.Model):
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    @staticmethod
    def add_to_cart(user, product, quantity=1):
        try:
            cart = Cart.objects.get(user=user)
        except:
            cart = Cart.objects.create(user=user)
        cart.save()
        contains = Contains.objects.create(cart=cart, product=product, quantity=quantity)
        Cart.update_total(cart).save()
        return contains

    @staticmethod
    def remove_item(pk):
        contains = Contains.objects.get(pk=pk)
        cart = contains.cart
        contains.delete()
        Cart.update_total(cart).save()