from django.shortcuts import render
from django.views.generic import TemplateView
from cart.models import Cart, Contains

# Create your views here.

class CartView(TemplateView):
    template_name = 'proto_cart/proto_cart_page.html'

    def get_context_data(self, **kwargs):
        data = super(CartView, self).get_context_data(**kwargs)
        cart = Cart.objects.get_or_create(user=self.request.user)
        try:
            contains_list = Contains.objects.get(cart=cart)
        except:
            contains_list = []
        data['purchase'] = cart
        data['cart'] = contains_list
        return data