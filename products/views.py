from django.shortcuts import render, get_object_or_404
from products.models import Products, ProductTag
from django.views.generic import TemplateView

# products = [{'name': 'Cocoa Puffs',
#              'description': 'Banned in Europe',
#              'price': 5.99,
#              'category': 'cereal',
#              'nutritional_info': 1,
#              'manufacturer': 2},
#
#             {'name': 'Lucky Charms',
#              'description': 'Banned in Iceland',
#              'price': 6.99,
#              'category': 'cereal',
#              'nutritional_info': 3,
#              'manufacturer': 4}
#             ]

# Create your views here.


def index(request):
    context = {'products' : Products.objects.all()}
    return render(request, 'proto_products/proto_products.html', context)

def get_product_by_tags(request):
    ''' GET request when loading the landing page

        :returns
        it renders the landing page, with a dictionary that contains tag and products list pair. for every tag, we list
        every product associated with that tag'''
    if request.method == 'GET':
        # TODO 1: get all tags
        tags = ProductTag.objects.all()
        # TODO 2: Create a dictionary, that maps every tag with list of products
        tag_maps_product_dict = {'tags_with_products' : {}}
        for tag in tags:
            if tag.listedas_set.all():
                tag_maps_product_dict['tags_with_products'][tag] = [x.product for x in tag.listedas_set.all()]
        # TODO 3: render landing page with dictionary
        return render(request, 'proto_landingpage.html', tag_maps_product_dict)

def get_product_by_id(request, id):
    return render(request, 'proto_products/proto_product_detail_page.html', {
        'product' : get_object_or_404(Products, pk=id)
    })


class ProductLogic(TemplateView):
    template = 'product/index.html'

    def get_context_data(self, **kwargs):
        data = super(ProductLogic, self).get_context_data(**kwargs)
        data['products'] = Products.objects.all().order_by('name')
        if self.request.GET.get('criteria') != "" and self.request.GET.get('criteria') != None:
            specified_criteria = self.request.GET.get('criteria')
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
        return data

    def get_all_unique_categories(self):
        all_products = Products.objects.all()
        all_unique_categories = []
        for elem in all_products:
            if elem.category not in all_unique_categories:
                all_unique_categories.append(elem.category)
        return sorted(all_unique_categories)