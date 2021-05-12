from django.test import TestCase

# Create your tests here.

class TestProductModels(TestCase):

    def setUp(self):
        self.nut_info = NutritionalInfo.objects.create(energy=0.1, sugar=0.2, fat=0.3, saturates=0.4)
        self.product = Products.objects.create(name="randy", short_description="very randy", description="lol",
                                               price=0.5, category="cereal", nutrional_info=self.nut_info, in_stock=10)
        self.url = "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cGljdHVyZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&w=1000&q=80"
        self.product_image = ProductImage.objects.create(image=self.url, product=self.product)

    def test_update_stock(self):
        Products.update_stock(self.product, 10) #removes 10 of product from stock
        self.assertEqual(self.product.in_stock, 0)

        Products.update_stock(self.product, 10, 0) #adds 10 of product to stock
        self.assertEqual(self.product.in_stock, 10)

    def test_get_products(self):
        product_list = Products.get_products() #we get the list of dictionaries

        # we check whether the amount of items in the dictonary are the right amount
        self.assertEqual(len(product_list[0]), 7)

        # we check for all keys in dictionary
        self.assertEqual(type(product_list[0]['id']), int)
        self.assertEqual(type(product_list[0]['name']), str)

    def test_get_detail_for_product(self):
        pk = self.product.id
        data = Products.get_detail_data_for_product(pk)
        self.assertEqual(len(data), 12)

    def test_get_first_image_for_each_product(self):
        pk = self.product.id
        product_image_dic = ProductImage.get_first_image_for_each_product()
        self.assertEqual(product_image_dic[pk], self.url)


