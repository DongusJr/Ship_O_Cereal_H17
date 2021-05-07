from django.shortcuts import render
from django.views.generic import TemplateView

from cart.forms.creditcard_form import PaymentForm
from cart.models import Cart, Contains

# Create your views here.

class CartView(TemplateView):
    template_name = 'proto_cart/proto_cart_page.html'

    def get_context_data(self, **kwargs):
        data = super(CartView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        contains_list = Contains.objects.filter(cart=cart)
        if self.request.method == 'DELETE':
            self.delete(self.request)
        if contains_list:
            data['has'] = True
        else:
            data['has'] = False
        data['purchase'] = cart
        data['cart'] = contains_list
        return data

    def delete(self, request):
        primary_key = request.DELETE.get('delete')
        Contains.remove_item(primary_key)
        return render('proto_cart/proto_cart_page.html')

class CredicCardField:
    pass


class CompletePurchase(TemplateView):
    template_name = 'proto_cart/proto_payment_form.html'

    def get_context_data(self, **kwargs):
        data = super(CompletePurchase, self).get_context_data(**kwargs)
        creditcard_form = PaymentForm()
        data['form'] = creditcard_form
        return data