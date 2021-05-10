from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from cart.forms.creditcard_form import PaymentForm
from cart.forms.personalinfo_form import PersonInfoForm
from cart.models import Cart, Contains

# Create your views here.
from users.models import PaymentInfo


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
    template_name = 'proto_cart/Complete_purchase/payment_template.html'
    html_template_names = {'payment' : 'proto_cart/Complete_purchase/proto_payment_form.html',
                           'person_info': 'proto_cart/Complete_purchase/proto_personinfo_form.html',
                           'review': 'proto_cart/Complete_purchase/proto_review.html',
                           'complete_order': 'proto_cart/Complete_purchase/proto_payment_successful.html'}

    def get(self, request, *args, **kwargs):
        step = self._get_step()
        print(step)
        if step is not None:
            form = self._get_form(step)
            print("was here")
            return render(request, self.template_name, {'form_html' : self.html_template_names[step], 'form': form})
        else:
            self.request.session['step'] = 'payment'
            return render(request, self.template_name, {'form_html' : self.html_template_names['payment']})

    def _get_step(self):
        if 'step' in self.request.GET:
            return self.request.GET['step']
        try:
            return self.request.session['step']
        except:
            return None

    def _get_form(self, step):
        if step == 'payment':
            try:
                return PaymentForm(data=self.request.session['payment_form'])
            except:
                return PaymentForm()
        if step == 'person_info':
            try:
                return PersonInfoForm(data=self.request.session['person_info_form'])
            except:
                return PersonInfoForm()
        return ''




    def post(self ,request, *args, **kwargs):
        print(f"POST: {request.POST}")
        if request.POST.get('personinfo_step') == 'Continue':
            form = PaymentForm(data=request.POST)
            self.request.session['payment_form'] = self.request.POST
            if form.is_valid():
                self.request.session['step'] = 'person_info'
        if request.POST.get('review_step') == 'Continue':
            form = PersonInfoForm(data=request.POST)
            self.request.session['person_info_form'] = self.request.POST
            if form.is_valid():
                self.request.session['step'] = 'review'
            else:
                print('form invalid')
        if request.POST.get('complete_order') == 'Complete order':
            payment_form, person_info_form = PaymentForm(self.request.session['payment_form']), PersonInfoForm(self.request.session['person_info_form'])
            payment_obj = payment_form.save()
            person_info_obj = person_info_form.save()
            user_cart = Cart.objects.get(user=self.request.user)
            user_cart.complete_cart(self.request.user.id, payment_obj, person_info_obj)
            del request.session['step']
            del request.session['payment_form']
            del request.session['person_info_form']
            return render(request, self.template_name, {'form_html': self.html_template_names['complete_order']})
        return redirect('complete_order')