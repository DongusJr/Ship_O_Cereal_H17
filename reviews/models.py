from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Products
from users.models import User

# Create your models here.
class Review(models.Model):
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])  # 1-10
    comment = models.CharField(max_length=512)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def has_made_review(user, product):
        '''
        has_made_review(user, product)

        parameters: user: User, product: Products,
        Checks if the given user has made a review for the given product
        '''
        try:
            if Review.objects.filter(user=user, product=product):
                return True
        except:
            return False

