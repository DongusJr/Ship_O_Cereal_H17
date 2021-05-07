from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from cart.models import Cart

def get_cart_number(request):
    try:
        cart_object = Cart.objects.get(user=request.user)
        cart_amount = cart_object.number_of_items
    except:
        cart_amount = 0

    return {'cart_amount': cart_amount}
