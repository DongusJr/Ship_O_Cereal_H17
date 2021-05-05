from django.shortcuts import render
from django.views.generic import TemplateView
from cart.models import Cart, Account, Contains

# Create your views here.

class CartView(TemplateView):
    template_name = 'proto_cart/proto_cart_page.html'

    def get_context_data(self, **kwargs):
        data = super(CartView, self).get_context_data(**kwargs)
        user = Account.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        contains_list = Contains.objects.get(cart=cart)
        data['purchase'] = cart
        data['cart'] = contains_list
        return data