import django.utils.datastructures
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from users.models import Order, Profile

# Create your views here.

def login_register(request):
    print(request.POST)
    if request.user.is_authenticated:
        return redirect('landing_page')
    register_form = UserCreationForm()
    login_form = AuthenticationForm()
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            login_form = AuthenticationForm(data=request.POST)
            success = _login(request)
            print("login success: " + str(success))
            if success:
                return redirect('product_index')
        elif request.POST.get('submit') == 'register':
            register_form = UserCreationForm(data=request.POST)
            success = _register(request)
            print("register success: " + str(success))
            if success:
                return redirect('landing_page')
    # return render(request, 'proto_users/account.html', {
    #     'form_1' : register_form,
    #     'form_2' : login_form
    # })
    return render(request, 'login_page.html', {
        'form_1' : register_form,
        'form_2' : login_form
    })

def _login(request):
    username = request.POST['username']
    try:
        password = request.POST['password']
    except django.utils.datastructures.MultiValueDictKeyError:
        password = request.POST['password1']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    else:
        return False

def _register(request):
    form = UserCreationForm(data=request.POST)
    if form.is_valid():
        form.save()
        user = authenticate(username=request.POST['username'], password=request.POST['password1'])
        user_profile = Profile(user=user,
                               image="https://www.edmundsgovtech.com/wp-content/uploads/2020/01/default-picture_0_0.png",
                               description=""
                               )
        user_profile.save()
        login_success = _login(request)
        if login_success:
            return True
    else:
        return False


# Create your views here.
class UserProfile(TemplateView):
    template_name = 'proto_account/proto_profile.html'

    def get_context_data(self, **kwargs):
        data = super(UserProfile, self).get_context_data(**kwargs)
        user_profile = Profile.objects.get(user=self.request.user)
        data['profile'] = user_profile
        order_history_dict = _create_order_dictionary_dict()
        # try:
        #     prev_ord = user.order
        # except:
        #     data['previous_order'] = None
        #     return data
        # data['previous_order'] = prev_ord
        # previous_order = Order.objects.get(prev=prev_ord)
        # dic = {}
        # for order in previous_order:
        #     dic[order] = OrderProduct.objects.get(order=order)
        # data['order'] = dic
        return data

    def _create_order_dictionary_dict(self):
