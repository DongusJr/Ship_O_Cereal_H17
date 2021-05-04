from django.test import TestCase
from products.models import Products, NutritionalInfo
from users.models import ZipCodes, User
from cart.models import Cart

# Create your tests here.
class TestCartModels(TestCase):
    def setUp(self):
        self.nut_in = NutritionalInfo.objects.create(energy=1.1, sugar=2.1, fat=3.1, saturates=4.1)
        self.product = Products.objects.create(name="lard", description="cool", price=6.99,
                                               category="awesome", nutritional_info=self.nut_in)
        self.zip = ZipCodes.objects.create(zip=100, city_name="Kyoto")
        self.cart = Cart.objects.create(product_list=[self.product], total=self.product.price)
        self.user = User.objects.create(session_id=1, username="bb bandit", password="asshole",
                                        email="cash@money.com", zip=self.zip, address="la Guardia",
                                        cart=self.cart)

    def test_add_to_cart(self):
        added_to_cart = self.cart.add_to_cart(self.product, 1)
        self.assertTrue(added_to_cart, True)
