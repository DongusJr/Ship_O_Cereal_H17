from django.db import models

import heapq
# Create your models here.
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404


class NutritionalInfo(models.Model):
    energy = models.FloatField()
    sugar = models.FloatField()
    fat = models.FloatField()
    saturates = models.FloatField()
    serving_amount = models.IntegerField(default=14)

    @staticmethod
    def update_nutritional_info(data, nut_obj):
        nut_obj.energy = data['energy']
        nut_obj.sugar = data['sugar']
        nut_obj.fat = data['fat']
        nut_obj.saturates = data['saturates']
        nut_obj.serving_amount = int(data['serving_amount'])
        nut_obj.save()
        return nut_obj

class Products(models.Model):
    name = models.CharField(max_length=64)
    short_description = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    price = models.FloatField()
    category = models.CharField(max_length=64)
    nutritional_info = models.ForeignKey(NutritionalInfo, on_delete=models.CASCADE)
    in_stock = models.IntegerField(default=1) #can not be less than zero

    def __str__(self):
        return self.name

    @staticmethod
    def update_product(data, product):
        product.name = data['name']
        product.short_description = data['short_description']
        product.description = data['description']
        product.price = data['price']
        product.category = data['category']
        product.nutritional_info = NutritionalInfo.update_nutritional_info(data['nutritional_info'], product.nutritional_info)
        ProductTag.update_tags(product, data['tags'])
        product.in_stock = data['in_stock']
        product.save()


    @staticmethod
    def update_stock(product, quantity, state=1):
        if state == 1:
            product.in_stock -= quantity
        else:
            product.in_stock += quantity

    @staticmethod
    def get_products(product_query=None):
        product_image_map = ProductImage.get_first_image_for_each_product()

        if product_query is None:
            product_query = Products.objects.all()
        products = [{'id': product.id,
                     'name': product.name,
                     'short_description': product.short_description,
                     'description': product.description,
                     'price': product.price,
                     'category': product.category,
                     'image': product_image_map[product.id]
                     }
                    for product in product_query]
        return products

    @staticmethod
    def get_detail_data_for_product(id):
        product = get_object_or_404(Products, pk=id)
        tags = ProductTag.objects.filter(product=product).values()
        data = {'name': product.name,
                'description': product.description,
                'short_description': product.short_description,
                'price': product.price,
                'category': product.category,
                'in_stock': product.in_stock,
                'energy': product.nutritional_info.energy,
                'sugar': product.nutritional_info.sugar,
                'fat': product.nutritional_info.fat,
                'saturates': product.nutritional_info.saturates,
                'serving_amount': product.nutritional_info.serving_amount,
                'tags': tags
                }
        return data


class ProductImage(models.Model):
    image = models.CharField(max_length=9999)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    @staticmethod
    def get_first_image_for_each_product():
        ''' Function that returns a dictionary where the key is a id of a product and
            the value is the first image in the database

            :returns
            product_image_map : dictionary{product_id : product_image}
        '''
        product_image_map = {}
        product_queryset = Products.objects.prefetch_related('productimage_set')
        for product in product_queryset:
            # Map product id with first image in the db associated with it
            try:
                product_image_map[product.id] = product.productimage_set.first().image
            except AttributeError:
                product_image_map[product.id] = ''
        return product_image_map


class ProductTag(models.Model):
    name = models.CharField(max_length=64)
    product = models.ManyToManyField(Products)

    def __str__(self):
        return self.name

    @staticmethod
    def select_all_related_products():
        ''' Function that returns a list with every tag and  every product that is associated with said tag.

            :returns
            tags : list[id, name, products]
                 : product_list[id, name, description, price, category, image]
        '''
        # Prefetch all products to reduce unnecessary queries
        tag_queryset = ProductTag.objects.prefetch_related('product')
        # Store all return data in this list
        tags = []

        # To reduce queries, already have a map between products and product image
        product_image_map = ProductImage.get_first_image_for_each_product()

        for tag in tag_queryset:
            # products associated with tag
            products = [{'id':product.id,
                         'name':product.name,
                         'short_description': product.short_description,
                         'description':product.description,
                         'price':product.price,
                         'category':product.category,
                         'image':product_image_map[product.id]
                         }
                        for product in tag.product.all()]
            # Add tag to return list
            tags.append({'id':tag.id, 'name':tag.name, 'products':products})
        return tags

    @staticmethod
    def get_products_with_tag(tag_name):
        tag = ProductTag.objects.get(name__iexact=(tag_name))
        tag_queryset = ProductTag.objects.prefetch_related('product')

        product_image_map = ProductImage.get_first_image_for_each_product()

        products = [{'id': product.id,
                     'name': product.name,
                     'description': product.description,
                     'price': product.price,
                     'category': product.category,
                     'image': product_image_map[product.id]
                     }
                    for product in tag.product.all()]
        return products

    @staticmethod
    def get_similar_products(product):
        tag_queryset = ProductTag.objects.prefetch_related('product').filter(product=product)
        product_count_dict = {}
        for tag in tag_queryset:
            for product_in_tag in tag.product.all():
                try:
                    product_count_dict[product_in_tag.id] += 1
                except:
                    product_count_dict[product_in_tag.id] = 1
        product_tag_pair = list(product_count_dict.items())
        product_tag_pair.sort(key=lambda x:x[1])

        org_product_id = product.id
        product_image_map = ProductImage.get_first_image_for_each_product()
        products_queryset = Products.objects.all()
        products_data = []
        while product_tag_pair:
            product_id, count = product_tag_pair.pop()
            if product_id != org_product_id:
                count_product = products_queryset.get(pk=product_id)
                products_data.append({'id': count_product.id,
                                      'name': count_product.name,
                                      'short_description': count_product.short_description,
                                      'description': count_product.description,
                                      'price': count_product.price,
                                      'category': count_product.category,
                                      'image': product_image_map[count_product.id]
                                      })
        return products_data


    @staticmethod
    def get_tags_for_product(product):
        tag_list = ProductTag.objects.filter(product=product)
        return tag_list

    @staticmethod
    def update_tags(product, tags):
        tag_list = ProductTag.get_tags_for_product(product)
        for tag in tag_list:
            if tag.name not in tags:
                rag = ProductTag.objects.get(name=tag.name)
                rag.product.add(product)
                rag.save()

