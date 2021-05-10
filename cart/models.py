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
        '''
        update_total(cart_object, total)

        parameters: cart_object: Cart, total: int
        The method takes in the cart object and finds all Contains objects associated with the
        cart. We then preceed to calculating the total of the cart.
        We then change the cart object's class variable total to reflect the calculated total.
        Then we return the cart object.
        '''
        contains_list = Contains.objects.filter(cart=cart_object)
        for item in contains_list:
            total += item.quantity*(item.product.price)
        cart_object.total = total
        return cart_object

    @staticmethod
    def update_number_of_items(cart_object):
        '''
        update_number_of_items(cart_object)

        parameters: cart_object: Cart
        The method takes in the cart_object which we then preceed to find all associated
        Contains objects then we find the length of the query set and update the Cart object
        and return the cart object
        '''
        contains_list = Contains.objects.filter(cart=cart_object)
        number = len(contains_list)
        cart_object.number_of_items = number
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
