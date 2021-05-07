from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from cart.forms.creditcard_form import PaymentForm
from cart.forms.personalinfo_form import PersonInfoForm
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
    template_names = {'payment': 'proto_cart/proto_payment_form.html',
                      'person_info': 'proto_cart/proto_personinfo_form.html'}

    def get(self, request, *args, **kwargs):
        creditcard_form = PaymentForm()
        return render(request, self.template_names['payment'], {'form' : creditcard_form})

    def post(self ,request, *args, **kwargs):
        print(request.POST)
        current_form = PaymentForm(request.POST)
        if request.POST.get('submit') == 'confirm_payment':
            if current_form.is_valid():
                # current_form.save()
                print("form saved")
                current_form = PersonInfoForm()
                return render(request, self.template_names['person_info'], {'form': current_form})
            else:
                return render(request, self.template_names['payment'], {'form': current_form})
        return render(request, self.template_names['payment'], {'form': current_form})

