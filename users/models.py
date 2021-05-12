from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

from products.models import Products, ProductImage
from django.contrib.auth.models import User

# Create your models here.
class ZipCodes(models.Model):
    zip = models.IntegerField()
    city_name = models.CharField(max_length=64)

class Country(models.Model):
    name = models.CharField(max_length=50)

class PersonInfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip = models.ForeignKey(ZipCodes, on_delete=models.CASCADE)
    Street = models.CharField(max_length=80)

class PaymentInfo(models.Model):
    full_name = models.CharField(max_length=80)
    card_number = models.CharField(max_length=16)
    year = models.IntegerField(validators=[MinValueValidator(datetime.now().year - 1), MaxValueValidator(datetime.now().year + 80)])
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    cvc = models.CharField(max_length=3)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=9999)
    description = models.CharField(max_length=512, blank=True)
    # One profile can have many orders

    @staticmethod
    def get_profile_info_for_user(user_id):
        '''
        get_profile_info_for_user(user_id)

        parameters: user_id: int
        this method finds the profile of an authenticated user and collects
        the information in a dictionary which is then returned
        '''
        try:
            profile = Profile.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.create(user=user)
        profile_information = {'id': profile.id,
                               'description': profile.description,
                               'image': profile.image,
                               'username': profile.user.username}
        return profile_information

    @staticmethod
    def update_img(image, user_id):
        '''
        update_img(image, user_id)

        parameters: image: string, user_id: int
        this method sets a new image for the user by first getting
        the profile associated with the user id and then saving the
        changes
        '''
        profile = Profile.objects.get(user_id=user_id)
        profile.image = image
        profile.save()

    @staticmethod
    def update_desc(desc, user_id):
        '''
        update_desc(desc, user_id)

        parameters: desc: string, user_id: int
        this method is similar to update image where we only
        update the profile's description and save
        '''
        profile = Profile.objects.get(user_id=user_id)
        profile.description = desc
        profile.save()

class Order(models.Model):
    total = models.IntegerField(default=0)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)  # Order can only have 1 profile
    person_info = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)
    delivery = models.BooleanField()
    product = models.ManyToManyField(Products)

    def __str__(self):
        return f"Order number {self.id}, for user {self.profile.username}"

    @classmethod
    def create_order(cls, payment_obj, person_info_obj, user_id, total, products, delivery=False):
        '''
        create_order(cls, payment_obj, person_info_obj, user_id, total, products, delivery)

        parameters: cls: class, payment_obj: PaymentInfoForm, person_info_obj: PersonInfoForm ,
        user_id: int, total: int, products: Product list, delivery: boolean
        the method retains the product list of a previous order and creates a new order class object instance which
        is associated with the user we then return the class instance
        '''
        user = User.objects.get(id=user_id)
        new_order = cls(total=total, profile=user, person_info=person_info_obj, payment_info=payment_obj, delivery=delivery)
        new_order.save()
        for product in products:
            new_order.product.add(product)
        return cls

    @staticmethod
    def get_order_history_for_user(user_id):
        ''' function that returns a list of dictionary that contains information on a order and products associated with it

            :returns
            orders : list[dict<id, total, products>]
                   : products : list[dict<id, name, price, image>]
        '''
        order_queryset = Order.objects.filter(profile_id=user_id).prefetch_related('product')

        product_image_map = ProductImage.get_first_image_for_each_product()
        orders = []
        for order in order_queryset:
            products = [{'id': product.id,
                         'name': product.name,
                         'price': product.price,
                         'image': product_image_map[product.id]
                         }
                        for product in order.product.all()]
            orders.append({'id':order.id, 'total': order.total, 'products': products})
        return orders

    # def order_total(self, order):
    #     total = 0
    #     contains = OrderProduct.objects.get(order=order)
    #     for product in contains:
    #         total += product.price * (product.quantity)
    #     order.total = total
    #     return total

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_searches = models.TextField(max_length=128)

    @staticmethod
    def add_to_search_history(text, user):
        '''
        add_to_search_history(text, user)

        parameters: text: string, user: User
        this method creates a new instance of
        '''
        SearchHistory.objects.create(previous_searches=text, user=user).save()


    @staticmethod
    def get_all_previous_searches(user):
        all_searches = SearchHistory.objects.filter(user=user)
        return all_searches