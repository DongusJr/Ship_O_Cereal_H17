from django.shortcuts import render
from products.models import Products
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
    return render(request, 'proto_products/proto_index.html', context)

class ProductIndex(TemplateView):
    template = 'product/index.html'

    def get_context_data(self, **kwargs):
        data = super(ProductIndex, self).get_context_data(**kwargs)
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

        return data