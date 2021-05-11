from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from cart.models import Cart

def get_cart_number(request):
    '''
    get_cart_number

    this method finds the cart associated with the user we then set the
    number of users in the cart if the user has not created a cart i.e.
    by adding a product object in the cart then we return 0 we return a
    dictionary object which contains the cart number of items

    Note: we use this as a global variable or session object for the user
    to always have the number of items in the cart visible
    '''
    try:
        cart_object = Cart.objects.get(user=request.user)
        cart_amount = cart_object.number_of_items
    except:
        cart_amount = 0

    return {'cart_amount': cart_amount}
