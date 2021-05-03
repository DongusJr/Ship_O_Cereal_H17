from django.test import TestCase
from products.models import Products, Cart
from users.models import User

# Create your tests here.
class TestModels(TestCase):

    def setUp(self):
        """setUp contains the class objects we create for the unit test.
            The class objects contain basic content which can be tested"""
        self.product_object = Products.objects.create(product_name="inflation", price=1000, description="lorem ipsum",
                                                     image=images.default, category="hurricane", nutritional_info=100)
        self.product_object2 = Products.objects.create(product_name="product2", price=2000, description="lorem ipsum",
                                                      image=images.default, categpry="hurricane", nutritional_info=100)
        self.cart_object = Cart.objects.create(product_list=[self.product_object], price=1000)
        self.user_object = User.objects.create(username="test_user", password="user", email="user@gmail.com",
                                                session_id=0, cart=self.cart_object)

    def test_user(self):
        self.assertEqual(self.user_object.username, "test_user")
        self.assertEqual(self.user_object.password, "user")
        self.assertEqual(self.user_object.email, "user@gmail.com")
        #self.assertEqual(self.user_object.session_id, 0)