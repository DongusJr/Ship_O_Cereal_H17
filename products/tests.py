from django.test import TestCase
from products.models import *

# Create your tests here.

class TestProductModels(TestCase):

    def setUp(self):
        self.nut_info = NutritionalInfo.objects.create(energy=0.1, sugar=0.2, fat=0.3, saturates=0.4)
        self.product = Products.objects.create(name="randy", short_description="very randy", description="lol",
                                               price=0.5, category="cereal", nutrional_info=self.nut_info, in_stock=10)

    def test_update_stock(self):
        Products.update_stock(self.product, 10) #removes 10 of product from stock
        self.assertEqual(self.product.in_stock, 0)

        Products.update_stock(self.product, 10, 0) #adds 10 of product to stock
        self.assertEqual(self.product.in_stock, 10)

    #def test_get_products(self):
