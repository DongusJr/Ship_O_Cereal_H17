from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class ProductTag(models.Model):
    name = models.CharField(max_length=64)

class NutritionalInfo(models.Model):
    energy = models.FloatField()
    sugar = models.FloatField()
    fat = models.FloatField()
    saturates = models.FloatField()

class Products(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    nutritional_info = models.ForgeignKey(NutritionalInfo, on_detele=models.CASCADE)

class ProductImage(models.Model):
    image = models.CharField(max_length=9999)
    product = models.ForgeignKey(Products, on_delete=models.CASCADE)

class ListedAs(models.Model):
    product = models.ForeignKey(Products)
    name = models.ForeignKey(ProductTag)

# Should be in its own app
# class Cart(models.Model):
#     product_list = ArrayField(models.ForeignKey(Products))
#     total = models.IntegerField()