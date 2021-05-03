from django.test import TestCase
from ship_o_cereal import TestCase
from ... import User
from ... import Product
from ... import Cart

# Create your tests here.
class TestModels(TestCase):

    def setUp(self):
        """setUp contains the class objects we create for the unit test.
            The class objects contain basic content which can be tested"""
        self.product_object = Product.objects.create(product_name="inflation", price=1000, description="lorem ipsum",
                                                     image=images.default, category="hurricane", nutritional_info=100)
        self.product_object2 = Product.objects.create(product_name="product2", price=2000, description="lorem ipsum",
                                                      image=images.default, categpry="hurricane", nutritional_info=100)
        self.cart_object = Cart.objects.create(product_list=[self.product_object], price=1000)
        self.user_object = User.objects.create(username="test_user", password="user", email="user@gmail.com",
                                                session_id=0, cart=self.cart_object)

    def test_user(self):
        self.assertEqual(self.user_object.username, "test_user")
        self.assertEqual(self.user_object.password, "user")
        self.assertEqual(self.user_object.email, "user@gmail.com")
        self.assertEqual(self.user_object.session_id, 0)

    def test_cart(self):
        self.assertEqual(self.cart_object.content, [self.product_object])
        self.assertEqual(self.cart_object.price, 1000)

    def test_add_product_to_cart(self):
        self.cart_object.add_product(self.product_object2)
        self.assertEqual(self.cart_object.product_list, [self.product_object, self.product_object2])
        self.assertEqual(self.cart_object.price, 3000)

    def test_remove_product_from_cart(self):
        self.cart_object.remove_product(self.product_object2)
        self.assertEqual(self.cart_object.product_list, [self.product_object])
        self.assertEqual(self.cart_object.price, 1000)

    def test_product(self):
        self.assertEqual(self.product_object.product_name, "inflation")
        self.assertEqual(self.product_object.price, 1000)