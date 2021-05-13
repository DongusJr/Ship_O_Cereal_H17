from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from cart.forms.creditcard_form import PaymentForm
from cart.forms.personalinfo_form import PersonInfoForm
from cart.models import Cart, Contains

# Create your views here.
from users.models import PaymentInfo, Country, ZipCodes


class CartView(TemplateView):
    '''
    CartView
    this view class enables the user to view cart and all the
    objects selected for that cart with also the functionality
    to delete items from the cart
    '''
    template_name = 'account/basket.html'
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
    template_name = 'account/purchase_steps/payment_template.html'
    html_template_names = {'payment' : 'account/purchase_steps/proto_payment_form.html',
                           'person_info': 'account/purchase_steps/proto_personinfo_form.html',
                           'review': 'account/purchase_steps/proto_review.html',
                           'complete_order': 'account/purchase_steps/proto_payment_successful.html'}

    def get(self, request, *args, **kwargs):
        '''
        get
        this method allows the user to get the current step via a helper function
        and a rendering of steps that have been completed
        '''
        step = self._get_step()
        data = {}
        if step is not None:
            form = self._get_form(step)
            if form == 'review':
                person_info = self._get_person_info_from_form(self.request.session['person_info_form'])
                order_with_products = Cart.get_products_from_cart_of_user_and_total(self.request.user.id)
                data = {'payment' : self.request.session['payment_form'], 'person_info': person_info, 'order_with_products': order_with_products}
            return render(request, self.template_name, {'form_html' : self.html_template_names[step], 'form': form, 'data': data})
        else:
            self.request.session['step'] = 'payment'
            return render(request, self.template_name, {'form_html' : self.html_template_names['payment']})

    def _get_person_info_from_form(self, person_info_form):
        country_name = get_object_or_404(Country, pk=person_info_form['country']).name
        zip_code = get_object_or_404(ZipCodes, pk=person_info_form['zip']).zip

        data = {'first_name': person_info_form['first_name'],
                'last_name': person_info_form['last_name'],
                'country': country_name,
                'zip': zip_code,
                'street': person_info_form['Street']}
        return data


    def _get_step(self):
        '''
        _get_step
        this method checks the get request for the step tag in the html
        and returns the step if it exists otherwise the request has the current step
        stored in the session of the user
        '''
        if 'step' in self.request.GET:
            return self.request.GET['step']
        try:
            return self.request.session['step']
        except:
            return None

    def _get_form(self, step):
        '''
        _get_form(step)
        this method has the parameter step which checks which step the user is currently on
        and returns the form which is applicable to said step however if no parameter is found then
        an empty string is returned
        '''
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
        if step == 'review':
            return 'review'

        return ''




    def post(self ,request, *args, **kwargs):
        '''
        post
        this method saves the post request of the form which the user has
        submitted so that the user can return and alter information or create
        new information for a form
        if the form reaches its last step and the user submits the correlating information
        needed than the user is redirected to the complete_order url
        '''
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
                pass
        if request.POST.get('complete_order') == 'Complete order':
            payment_form, person_info_form = PaymentForm(self.request.session['payment_form']), PersonInfoForm(self.request.session['person_info_form'])
            payment_obj = payment_form.save()
            person_info_obj = person_info_form.save()
            user_cart = Cart.objects.get(user=self.request.user)
            user_cart.complete_cart(self.request.user.id, payment_obj, person_info_obj)
            del request.session['step']
            del request.session['payment_form']
            del request.session['person_info_form']
            return render(request, 'account/purchase_steps/proto_payment_successful.html', {})
        return redirect('complete_order')
