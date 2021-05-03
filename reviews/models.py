from django.db import models
from products.models import Products
from users.models import User

# Create your models here.
class Review(models.Model):
    rating = models.IntegerField(validators=[models.MinValueValidator(1), models.MaxValueValidator(10)])  # 1-10
    comment = models.CharField(max_length=512)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)