from django.shortcuts import render, get_object_or_404
from products.models import Products, ProductTag
from django.views.generic import TemplateView
from cart.models import Contains, ProductViewed
from django import template
from users.models import SearchHistory

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
        products= Products.objects.all()
        if 'tag' in self.request.GET:
            tags_in_use = self.request.GET.getlist('tag')
            data['tags'] = ProductTag.objects.exclude(name__in=tags_in_use)
            for tag in tags_in_use:
                products = products.filter(producttag__name=tag)
        else:
            data['tags'] = ProductTag.objects.all()

        if 'name' in self.request.GET:
            name_order = self.request.GET.get('name')
            if name_order == 'ascending':
                products = products.order_by('name')[::-1]
            elif name_order == 'descending':
                products = products.order_by('name')

        if 'price' in self.request.GET:
            order = self.request.GET['price']
            if order == 'descending':
                products = products.order_by('price')
            elif order == 'ascending':
                products = products.order_by('-price')

        if 'criteria' in self.request.GET:
            criteria = self.request.GET.get('criteria')
            if criteria != '':
                products = products.filter(name__icontains=criteria)

        if 'category' in self.request.GET:
            list_of_all_categories = self.get_all_unique_categories()
            category = self.request.GET['category']
            print(category)
            if category in list_of_all_categories:
                data['category'] = category
                products = products.filter(category__exact=category)

        data['category'] = 'Cereal'
        data['products'] = Products.get_products(products)
        return data

    def get_all_unique_categories(self):
        all_products = Products.objects.all()
        all_unique_categories = []
        for elem in all_products:
            if elem.category not in all_unique_categories:
                all_unique_categories.append(elem.category)
        return sorted(all_unique_categories)


class SingleProduct(TemplateView):
    template_name = 'proto_products/proto_product_detail_page.html'

    def get_context_data(self, **kwargs):
        data = super(SingleProduct, self).get_context_data(**kwargs)
        id = self.kwargs['id']
        product = get_object_or_404(Products, pk=id)
        ProductViewed.add_to_previously_viewed(product, self.request.user).save()
        data['product'] = product
        if 'quant' in self.request.GET:
            quantity = self.request.GET.get('quant')
            Contains.add_to_cart(self.request.user, product, int(quantity)).save()
            data['success'] = True

        return data