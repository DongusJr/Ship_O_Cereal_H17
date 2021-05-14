from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from cart.forms.creditcard_form import PaymentForm
from cart.forms.personalinfo_form import PersonInfoForm
from cart.models import Cart, Contains

# Create your views here.
from users.models import PaymentInfo, Country


class CartView(TemplateView):
    '''
    CartView
    this view class enables the user to view cart and all the
    objects selected for that cart with also the functionality
    to delete items from the cart
    '''
    template_name = 'account/cart/basket.html'
    data = {}

    def get(self, request, *args, **kwargs):
        '''
        get
        this method gets the cart for a specified user
        and then proceeds to filling the data to be sent
        in the render request
        '''
        cart = Cart.get_or_create_cart(self.request.user.id)
        contains_list = Contains.objects.filter(cart=cart)
        self.data['purchase'] = cart
        self.data['cart'] = contains_list
        self.data['has'] = self.helper()
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        '''
        post
        this method gets the Contains object which is to
        be deleted and then deleted and update the contents of the cart
        '''
        primary_key = request.POST.get('delete')
        if Contains.contains_exist(primary_key):
            Contains.remove_item(primary_key)
        cart = Cart.objects.get(user=request.user)
        self.data['cart'] = Contains.objects.filter(cart=self.data['purchase'])
        self.data['has'] = self.helper()
        self.data['purchase'] = Cart.update_total(cart)
        return render(request, self.template_name, self.data)

    def helper(self):
        '''
        helper
        this helper class function is used by both get and post
        to limit duplication of code; we check in the helper function
        whether the cart is empty or not
        '''
        if self.data['cart'] != []:
            return True
        else:
            return False


class CompletePurchase(TemplateView):
    '''
    CompletePurchase
    this view allows the user to render the pages pretaining to all the steps of
    a payment process and empties the cart object associated with the user
    '''
    login_required = True
    template_name = 'account/purchase_steps/payment_template.html'
    html_template_names = {'payment' : 'account/purchase_steps/payment_form.html',
                           'person_info': 'account/purchase_steps/personinfo_form.html',
                           'review': 'account/purchase_steps/review.html',
                           'complete_order': 'account/purchase_steps/payment_successful.html'}

    def get(self, request, *args, **kwargs):
        request.session['order_complete'] = False
        user_cart = Cart.objects.get(user=self.request.user)
        if not Cart.has_products(user_cart):
            return redirect('cart_page')
        data = dict()
        if 'step' in request.GET:
            step = request.GET.get('step')

            if step == 'payment':
                if 'payment' in request.session:
                    data = request.session['payment']
                return render(request, self.template_name, {'form_html': self.html_template_names['payment'], 'data': data})

            if step == 'person_info':
                if request.session['payment_done']:
                    countries = Country.objects.all()
                    if 'person_info' in request.session:
                        data = request.session['person_info']
                    return render(request, self.template_name, {'form_html': self.html_template_names['person_info'], 'data': data, 'countries': countries})


            if step == 'review':
                person_info = self._get_person_info_from_form(self.request.session['person_info'])
                order_with_products = Cart.get_products_from_cart_of_user_and_total(self.request.user.id)
                data = {'payment': self.request.session['payment'], 'person_info': person_info, 'order_with_products': order_with_products}
                return render(request, self.template_name, {'form_html': self.html_template_names['review'], 'data': data})

        try:
            data = request.session['payment']
        except:
            data = []
        return render(request, self.template_name, {'form_html': self.html_template_names['payment'], 'data': data})

    def post(self, request, *args, **kwargs):
        step = request.POST.get('step')

        if step == 'payment':
            form = PaymentForm(data=request.POST)
            if form.is_valid():
                request.session['payment'] = request.POST
                request.session['payment_done'] = True
                countries = Country.objects.all()
                try:
                    data = request.session['person_info']
                except:
                    data = dict()
                return render(request, self.template_name, {'form_html': self.html_template_names['person_info'], 'data': data ,'countries': countries})

        if step == 'person_info':
            form = PersonInfoForm(data=request.POST)
            if form.is_valid():
                self.request.session['person_info'] = self.request.POST
                data = self._get_review_data()
                request.session['person_info_done'] = True
                return render(request, self.template_name, {'form_html': self.html_template_names['review'], 'data':data})
            else:
                countries = Country.objects.all()
                return render(request, self.template_name, {'form_html': self.html_template_names['person_info'], 'countries': countries, 'data':request.POST})

        if step == 'review':
            if not request.session['order_complete']:
                data = self._get_review_data()
                payment_form, person_info_form = PaymentForm(self.request.session['payment']), PersonInfoForm(self.request.session['person_info'])
                payment_obj = payment_form.save()
                person_info_obj = person_info_form.save()
                user_cart = Cart.objects.get(user=self.request.user)
                user_cart.complete_cart(self.request.user.id, payment_obj, person_info_obj)
                del request.session['payment_done']
                del request.session['person_info_done']
            else:
                return redirect('profile')
            request.session['order_complete'] = True
            return render(request, 'account/purchase_steps/payment_successful.html', {'data': data})
        return render(request, self.template_name, {'form_html': self.html_template_names[step]})

    def _get_person_info_from_form(self, person_info_form):
        country_name = get_object_or_404(Country, pk=person_info_form['country']).name

        data = {'first_name': person_info_form['first_name'],
                'last_name': person_info_form['last_name'],
                'country': country_name,
                'zip': person_info_form['zip'],
                'city_name': person_info_form['city_name'],
                'street': person_info_form['Street']}
        return data

    def _get_review_data(self):
        person_info = self._get_person_info_from_form(self.request.session['person_info'])
        order_with_products = Cart.get_products_from_cart_of_user_and_total(self.request.user.id)
        return {'payment': self.request.session['payment'],
                'person_info': person_info,
                'order_with_products': order_with_products}
