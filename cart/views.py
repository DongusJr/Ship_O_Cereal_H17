from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from cart.forms.creditcard_form import PaymentForm
from cart.forms.personalinfo_form import PersonInfoForm
from cart.models import Cart, Contains

# Create your views here.

class CartView(TemplateView):
    template_name = 'proto_cart/proto_cart_page.html'
    data = {}

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        contains_list = Contains.objects.filter(cart=cart)
        self.data['purchase'] = cart
        self.data['cart'] = contains_list
        self.data['has'] = self.helper()
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        primary_key = request.POST.get('delete')
        Contains.remove_item(primary_key)
        cart = Cart.objects.get(user=request.user)
        self.data['cart'] = Contains.objects.filter(cart=self.data['purchase'])
        self.data['has'] = self.helper()
        self.data['purchase'] = Cart.update_total(cart)
        return render(request, self.template_name, self.data)

    def helper(self):
        if self.data['cart'] != []:
            return True
        else:
            return False

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

