from django.db import models
from products.models import Products
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

class Order(models.Model):
    total = models.IntegerField(default=0)
    profile = models.ForeignKey(User, on_delete=models.CASCADE) # Order can only have 1 profile
    person_info = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)
    delivery = models.BooleanField()

    def order_total(self, order):
        total = 0
        contains = OrderProduct.objects.get(order=order)
        for product in contains:
            total += product.price * (product.quantity)
        order.total = total
        return total

class OrderProduct(models.Model):
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=9999)
    description = models.CharField(max_length=512, blank=True)
    # One profile can have many orders
