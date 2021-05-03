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
    nutritional_info = models.ForeignKey(NutritionalInfo, on_delete=models.CASCADE)
    # manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

class ProductImage(models.Model):
    image = models.CharField(max_length=9999)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class ListedAs(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.ForeignKey(ProductTag, on_delete=models.CASCADE)

# class Review(models.Model):
#     rating = models.IntegerField(validators=[models.MinValueValidator(1), models.MaxValueValidator(10)])  # 1-10
#     comment = models.CharField(max_length=512)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

# Should be in its own app
# class Cart(models.Model):
#     product_list = ArrayField(models.ForeignKey(Products))
#     total = models.IntegerField()