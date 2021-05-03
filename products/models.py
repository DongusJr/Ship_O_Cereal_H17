from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Products(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    nutritional_info = models.IntegerField()
    image = models.ForeignKey(Images)

class Images(models.Model):
    url = ArrayField(max_length=3)

class Cart(models.Model):
    product_list = ArrayField(models.ForeignKey(Products))
    total = models.IntegerField()