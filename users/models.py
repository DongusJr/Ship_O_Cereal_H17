from django.db import models
from products.models import Cart

# Create your models here.
class ZipCodes(models.Model):
    zip = models.IntegerField()
    city_name = models.CharField(max_length=64)


class User(models.Model):
    session_id = models.IntegerField()
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=256, unique=True)
    zip = models.ForeignKey(ZipCodes)
    address = models.CharField(max_length=128)
    cart = models.ForeignKey(Cart)