from django.db import models
from cart.models import Cart
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class ZipCodes(models.Model):
    zip = models.IntegerField()
    city_name = models.CharField(max_length=64)

class Order(models.Model):
    product_list = ArrayField()
    total = models.IntegerField()

class PreviousOrders(models.Model):
    order_list = ArrayField(models.ForeignKey(Order))

    def create_order(self,  prev_ord, product_list, total):
        new_order = Order.create(product_list, total)
        prev_ord.order_list.append(new_order)

class User(models.Model):
    session_id = models.IntegerField()
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=256, unique=True)
    zip = models.ForeignKey(ZipCodes)
    address = models.CharField(max_length=128)
    cart = models.ForeignKey(Cart)
    order = models.ForeignKey(PreviousOrder)