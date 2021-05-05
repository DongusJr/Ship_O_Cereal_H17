from django.db import models
from products.models import Products
from django.contrib.auth.models import User

# Create your models here.
class ZipCodes(models.Model):
    zip = models.IntegerField()
    city_name = models.CharField(max_length=64)

class PreviousOrders(models.Model):
    total_purchases = models.IntegerField()

    def total_orders_made(self, prev):
        orders = Order.objects.get(prev=prev)
        i = 0
        for order in orders:
            i += 1
        prev.total_purchases = i

class Order(models.Model):
    total = models.IntegerField()
    prev = models.ForeignKey(PreviousOrders, on_delete=models.CASCADE)

    def order_total(self, order):
        total = 0
        contains = OrderProduct.objects.get(order=order)
        for product in contains:
            total += product.price * (product.quantity)
        order.total = total
        return total

class OrderProduct(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=256, unique=True)
    zip = models.ForeignKey(ZipCodes, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    order = models.ForeignKey(PreviousOrders, on_delete=models.CASCADE)