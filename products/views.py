from django.shortcuts import render, get_object_or_404
from products.models import Products, ProductTag
from django.views.generic import TemplateView
from cart.models import Contains, ProductViewed
from users.models import SearchHistory
from reviews.models import Review

# Create your views here.

def get_product_by_tags(request):
    if request.method == 'GET':
        tags_with_products = ProductTag.select_all_related_products()
        context = {'tags_with_products' : tags_with_products}
        print(context)
        return render(request, 'main_page.html', context)

class ProductLogic(TemplateView):
    template_name = 'proto_products/proto_products.html'

    def get_context_data(self, **kwargs):
        data = super(ProductLogic, self).get_context_data(**kwargs)
        data['products'] = Products.get_products()
        data['tags'] = ProductTag.objects.all()
        print(self.request)
        if 'name' in self.request.GET:
            name_order = self.request.GET.get('name')
            if name_order == 'ascending':
                data['products'] = data['products'].order_by('name')[::-1]
            elif name_order == 'descending':
                data['products'] = data['products'].order_by('name')
        if self.request.GET.get('criteria') != "" and self.request.GET.get('criteria') != None:
            specified_criteria = self.request.GET.get('criteria')
            try:
                SearchHistory.add_to_search_history(specified_criteria, self.request.user).save()
            except:
                pass
            data['products'] = data['products'].filter(name__icontains=specified_criteria)
        if 'price' in self.request.GET:
            order = self.request.GET['price']
            if order == 'descending':
                data['products'] = data['products'].order_by('price')
            elif order == 'ascending':
                data['products'] = data['products'].order_by('-price')

        if 'category' in self.request.GET:
            list_of_all_categories = self.get_all_unique_categories()
            category = self.request.GET['category']
            if category in list_of_all_categories:
                data['products'] = data['products'].filter(category__exact=category)

        if 'tag' in self.request.GET:
            tag = self.request.GET['tag'].lower()
            products = ProductTag.get_products_with_tag(tag)
            print(products)
            # all_products_with_tag = self.get_all_unique_tags(tags, tag)
            # new_list = []
            # for elem in data['products']:
            #     if elem in all_products_with_tag:
            #         new_list.append(elem)
            data['products'] = products
        return data

    def get_all_unique_categories(self):
        all_products = Products.objects.all()
        all_unique_categories = []
        for elem in all_products:
            if elem.category not in all_unique_categories:
                all_unique_categories.append(elem.category)
        return sorted(all_unique_categories)

    def get_all_unique_tags(self, tags, tag):
        all_products_with_tag = []
        for elem in tags:
            if elem.tag.name.lower() == tag:
                all_products_with_tag.append(elem.product)
        return all_products_with_tag

class SingleProduct(TemplateView):
    template_name = 'proto_products/proto_product_detail_page.html'
    data = {}

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        product = get_object_or_404(Products, pk=id)
        ProductViewed.add_to_previously_viewed(product, self.request.user).save()
        self.data['product'] = product
        if 'quant' in self.request.GET:
            quantity = self.request.GET.get('quant')
            Contains.add_to_cart(self.request.user, product, int(quantity)).save()
            self.data['success'] = True
        all_reviews = Review.objects.filter(product=product)
        if all_reviews:
            self.data['reviews'] = all_reviews
        else:
            self.data['reviews'] = None
        self.data['rating'] = self.calculate_mean_rating(product)
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        product = Products.objects.get(id=kwargs['id'])
        review_object = Review.objects.create(user=request.user, product=product)
        if 'rating' in request.POST and review_object.rating:
            rating = request.POST.get('rating')
            if rating:
                if int(rating) > 10:
                    rating = 10
                elif int(rating) < 1:
                    rating = 1
                review_object.rating = rating
                review_object.save()
        if 'review' in self.request.POST and review_object.comment:
            review = self.request.POST.get('review')
            if review:
                review_object.comment = review
                review_object.save()
        self.data['reviews'] = Review.objects.filter(product=product)
        self.data['rating'] = self.calculate_mean_rating(product)
        return render(request, self.template_name, self.data)

    def calculate_mean_rating(self, product):
        review_objects = Review.objects.filter(product=product)
        rating = 0
        for review in review_objects:
            rating += review.rating
        return round(rating/len(review_objects))
