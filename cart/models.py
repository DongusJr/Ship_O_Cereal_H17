from django.contrib.auth.models import User
from django.db import models
from products.models import Products
from users.models import Order

# Create your models here.

class Cart(models.Model):
    # Possibly have user id
    total = models.IntegerField(default=0)
    number_of_items = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @staticmethod
    def update_total(cart_object, total=0):
        contains_list = Contains.objects.filter(cart=cart_object)
        for item in contains_list:
            total += item.quantity*(item.product.price)
        cart_object.total = total
        cart_object.save()
        return cart_object

    @staticmethod
    def update_number_of_items(cart_object):
        contains_list = Contains.objects.filter(cart=cart_object)
        number = len(contains_list)
        cart_object.number_of_items = number
        cart_object.save()
        return cart_object

    def complete_cart(self, user_id, payment_obj, person_info_obj):
        try:
            cart = Cart.objects.get(user=user_id)
        except:
            return False
        contains_of_cart = Contains.objects.filter(cart=cart)
        products = []
        print(products)
        for contain in contains_of_cart:
            products.append(contain.product)
            contain.delete()
        Order.create_order(payment_obj, person_info_obj, user_id, cart.total, products)
        Cart.update_total(cart)
        Cart.update_number_of_items(cart)
        return True

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
        Cart.update_number_of_items(cart).save()
        return contains

    @staticmethod
    def remove_item(pk):
        contains = Contains.objects.get(pk=pk)
        cart = contains.cart
        contains.delete()
        Cart.update_total(cart).save()
        Cart.update_number_of_items(cart).save()


class ProductViewed(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def add_to_previously_viewed(product, user):
        try:
            ProductViewed.objects.get(user=user, product=product)
            ProductViewed.objects.get(user=user, product=product).delete()
        except:
            pass
        return ProductViewed.objects.create(user=user, product=product)

    @staticmethod
    def get_all_viewed_products(user):
        return ProductViewed.objects.filter(user=user)
