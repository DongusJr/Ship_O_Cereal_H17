from django.db import models

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
    price = models.FloatField()
    category = models.CharField(max_length=64)
    nutritional_info = models.ForeignKey(NutritionalInfo, on_delete=models.CASCADE)
    # in_stock = models.IntegerField(validators=[models.MinValueValidator(1)], default=10)#can not be less than zero
    # manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    # @staticmethod
    # def update_stock(product, quantity, state=1):
    #     if state == 1:
    #         product.in_stock -= quantity
    #     else:
    #         product.in_stock += quantity

class ProductImage(models.Model):
    image = models.CharField(max_length=9999)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class ListedAs(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.ForeignKey(ProductTag, on_delete=models.CASCADE)

# Should be in its own app
