from django.shortcuts import render
from products.models import Products

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