from django.shortcuts import render
from django.views.generic import TemplateView
from cart.models import Cart, Contains

# Create your views here.

class CartView(TemplateView):
    template_name = 'proto_cart/proto_cart_page.html'

    def get_context_data(self, **kwargs):
        data = super(CartView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        contains_list = Contains.objects.filter(cart=cart)
        if 'remove' in self.request.GET:
            primary_key = self.request.GET.get('remove')
            Contains.remove_item(primary_key)
        data['has'] = True
        data['purchase'] = cart
        data['cart'] = contains_list
        return data