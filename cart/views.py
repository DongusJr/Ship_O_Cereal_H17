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
        if contains_list:
            data['has'] = True
        else:
            data['has'] = False
        data['purchase'] = cart
        data['cart'] = contains_list
        return data

class CartItems(TemplateView):
    template_name = 'proto_base.html'

    def get_context_data(self, **kwargs):
        data = super(CartItems, self).get_context_data(**kwargs)
        cart = Cart.objects.get_object_or_404(user=self.request.user)
        print(cart)
        data['number'] = cart.number_of_items
        return data