from django.db import models
from django.db.models import Prefetch

from products.models import Products, ProductImage
from django.contrib.auth.models import User

# Create your models here.
class ZipCodes(models.Model):
    zip = models.IntegerField()
    city_name = models.CharField(max_length=64)

class Country(models.Model):
    name = models.CharField(max_length=50)

class PersonInfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip = models.ForeignKey(ZipCodes, on_delete=models.CASCADE)
    Street = models.CharField(max_length=80)

class PaymentInfo(models.Model):
    full_name = models.CharField(max_length=80)
    card_number = models.IntegerField()
    expiration_date = models.IntegerField()
    cvc = models.IntegerField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=9999)
    description = models.CharField(max_length=512, blank=True)
    # One profile can have many orders

    @staticmethod
    def get_profile_info_for_user(user_id):
        profile = Profile.objects.filter(user_id=user_id)[0]
        profile_information = {'id': profile.id,
                               'description': profile.description,
                               'image': profile.image,
                               'username': profile.user.username}
        return profile_information


class Order(models.Model):
    total = models.IntegerField(default=0)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)  # Order can only have 1 profile
    person_info = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)
    delivery = models.BooleanField()
    product = models.ManyToManyField(Products)

    def __str__(self):
        return f"Order number {self.id}, for user {self.profile.username}"

    @staticmethod
    def get_order_history_for_user(user_id):
        ''' function that returns a list of dictionary that contains information on a order and products associated with it

            :returns
            orders : list[dict<id, total, products>]
                   : products : list[dict<id, name, price, image>]
        '''
        order_queryset = Order.objects.prefetch_related(
            Prefetch('profile', queryset=Profile.objects.filter(user_id=user_id)))

        product_image_map = ProductImage.get_first_image_for_each_product()
        orders = []
        for order in order_queryset:
            products = [{'id': product.id,
                         'name': product.name,
                         'price': product.price,
                         'image': product_image_map[product.id]
                         }
                        for product in order.product.all()]
            orders.append({'id':order.id, 'total': order.total, 'products': products})
        return orders

    # def order_total(self, order):
    #     total = 0
    #     contains = OrderProduct.objects.get(order=order)
    #     for product in contains:
    #         total += product.price * (product.quantity)
    #     order.total = total
    #     return total