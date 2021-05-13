from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from products.forms.productform import ProductCreateForm, ProductUpdateForm
from products.models import Products, ProductTag, ProductImage, NutritionalInfo
from django.views.generic import TemplateView
from cart.models import Contains, ProductViewed
from django import template
from users.models import SearchHistory
from reviews.models import Review

# Create your views here.




def get_product_by_tags(request):
    return render(request, 'main_page.html', {})

def get_tags_json(request):
    if request.method == 'GET':
        tags_with_products = ProductTag.select_all_related_products()

        return JsonResponse({'data': tags_with_products})


class ProductLogic(TemplateView):
    template_name = 'proto_products/proto_products.html'

    def get_context_data(self, **kwargs):
        data = super(ProductLogic, self).get_context_data(**kwargs)
        data['all_categories'] = self.get_all_unique_categories()
        products= Products.objects.all()

        if 'tag' in self.request.GET:
            tags_in_use = self.request.GET.getlist('tag')
            data['tags'] = ProductTag.objects.exclude(name__in=tags_in_use)
            data['active_tags'] = ProductTag.objects.filter(name__in=tags_in_use)
            for tag in tags_in_use:
                products = products.filter(producttag__name=tag)
        else:
            data['tags'] = ProductTag.objects.all()

        if self.request.GET.getlist('urlencode'):
            tags_in_use = self._get_tags_from_url(self.request.GET.getlist('urlencode')[0])
            if tags_in_use != ['']:
                data['tags'] = ProductTag.objects.exclude(name__in=tags_in_use)
                data['active_tags'] = ProductTag.objects.filter(name__in=tags_in_use)
                for tag in tags_in_use:
                    products = products.filter(producttag__name=tag)

        if 'criteria' in self.request.GET:
            criteria = self.request.GET.get('criteria')
            if criteria != '':
                if products != []:
                    products = products.filter(name__icontains=criteria)
                if str(self.request.user) != 'AnonymousUser':
                    SearchHistory.add_to_search_history(criteria, self.request.user)

        if 'category' in self.request.GET:
            category = self.request.GET['category']
            if category in data['all_categories']:
                data['category'] = category
                if products != []:
                    products = products.filter(category__exact=category)

        if 'order' in self.request.GET and products!=[]:
            order = self.request.GET.get('order')
            if order == 'name_ascending':
                products = products.order_by('name')[::-1]
            elif order == 'name_descending':
                products = products.order_by('name')
            elif order == 'price_descending':
                products = products.order_by('price')
            elif order == 'price_ascending':
                products = products.order_by('-price')

        page = self.request.GET.get('page', 1)
        products_paginated = self._paginate_data(products, page, 10)

        data['pages'] = products_paginated
        data['products'] = Products.get_products(products_paginated)

        return data

    def _get_tags_from_url(self, urlencode):
        tags_in_use = []
        tag_name = ""
        tag_begin = False
        for letter in urlencode:
            if letter == "&":
                tags_in_use.append(tag_name)
                tag_name = ""
                tag_begin = False
            elif tag_begin:
                tag_name += letter if letter != '+' else " "
            elif letter == '=':
                tag_begin = True
        tags_in_use.append(tag_name)
        return tags_in_use


    def _paginate_data(self, data_list, page, num_per_page):
        paginator = Paginator(data_list, num_per_page)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        return data



    def get_all_unique_categories(self):
        all_products = Products.objects.all()
        all_unique_categories = []
        for elem in all_products:
            if elem.category not in all_unique_categories:
                all_unique_categories.append(elem.category)
        return sorted(all_unique_categories)


class SingleProduct(TemplateView):
    template_name = 'products/single_product_page.html'
    data = {}

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        product = get_object_or_404(Products, pk=id)

        if str(self.request.user) != 'AnonymousUser':
            ProductViewed.add_to_previously_viewed(product, self.request.user).save()
        self.data['product'] = product

        if 'quant' in self.request.GET:
            quantity = self.request.GET.get('quant')
            Contains.add_to_cart(self.request.user, product, int(quantity)).save()
            self.data['success'] = True

        all_reviews = Review.objects.filter(product=product)
        if all_reviews:
            self.data['reviews'] = all_reviews
            self.data['rating'] = self.calculate_mean_rating(product)
        else:
            self.data['reviews'] = None

        similar_tag = []
        tags = ProductTag.objects.filter(product=product)
        for tag in tags:
            if len(similar_tag) <= 10:
                similar_tag.extend(ProductTag.get_products_with_tag(tag.name))
            else:
                break
        self.data['similar_products'] = similar_tag
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        product = Products.objects.get(id=kwargs['id'])
        review_object = Review.objects.create(user=request.user, product=product)
        if 'rate' in request.POST and review_object.rating:
            rating = request.POST.get('rate')
            review_object.rating = rating
            review_object.save()
        if 'review' in self.request.POST:
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
        return float(round(2 * (rating/len(review_objects)))/2)


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            nutritional_info = NutritionalInfo(energy=request.POST['energy'],
                                               sugar=request.POST['sugar'],
                                               fat=request.POST['fat'],
                                               saturates=request.POST['saturates'],
                                               serving_amount=request.POST['serving_amount'])
            nutritional_info.save()
            product = Products(name=request.POST['name'],
                               short_description=request.POST['short_description'],
                               description=request.POST['description'],
                               price=request.POST['price'],
                               category=request.POST['category'],
                               nutritional_info=nutritional_info,
                               in_stock=request.POST['in_stock'],)
            product.save()
            for tag_id in request.POST.getlist('tags'):
                tag = ProductTag.objects.get(id=tag_id)
                tag.product.add(product)
            product_image = ProductImage(image=request.POST['image'], product=product)
            product_image.save()
            return redirect('product_index')
    else:
        form = ProductCreateForm()
    return render(request, 'proto_products/proto_create_product.html', {
        'form': form
    })

@login_required
def update_product(request, id):
    product_data = Products.get_detail_data_for_product(id)
    if request.method == 'POST':
        # form = ProductUpdateForm(data=data)
        # if form.is_valid():
        #     print("VALID UPDATE")
        pass
    else:
        form = ProductUpdateForm(data=product_data)
    return render(request, 'proto_products/proto_update_product.html', {
        'form': form,
        'id': id
    })