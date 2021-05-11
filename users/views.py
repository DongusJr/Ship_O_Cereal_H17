import django.utils.datastructures
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from products.models import ProductImage
from users.models import Order, Profile, SearchHistory
from cart.models import ProductViewed

# Create your views here.

def login_register(request):
    '''
    login_register
    this method allows the user to login to an already registered account
    if the user session has already an authenticated user then we redirect to the
    profile otherwise we render the appropriate forms and then get all the information
    inputted by the user we then render the forms on the url
    '''
    if request.user.is_authenticated:
        return redirect('profile')
    register_form = UserCreationForm()
    login_form = AuthenticationForm()
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            login_form = AuthenticationForm(data=request.POST)
            success = _login(request)
            if success:
                return redirect('product_index')
        elif request.POST.get('submit') == 'register':
            register_form = UserCreationForm(data=request.POST)
            success = _register(request)
            if success:
                return redirect('profile')
    # return render(request, 'proto_users/account.html', {
    #     'form_1' : register_form,
    #     'form_2' : login_form
    # })
    return render(request, 'account/login_page.html', {
        'form_1' : register_form,
        'form_2' : login_form
    })

def _login(request):
    '''
    login
    this method gets the inputted username and password by the user
    we then authenticate the user and return True if successfull otherwise
    False
    '''
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
    '''
    _register
    this method gets the form for the user creation and input the
    inputted information into the form then we save and authenticate the user
    and create a profile for the user and save lastly we log the user in
    if successfull we return True else we return False
    '''
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
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        '''
        get_context_data

        this method gets all information for the user and all searches the user
        has previously viewed and limit the list to the top ten and the order history
        of the user
        '''
        user_id = self.request.user.id
        data = super(UserProfile, self).get_context_data(**kwargs)
        user_profile = Profile.get_profile_info_for_user(user_id)
        data['profile'] = user_profile
        order_history_list = Order.get_order_history_for_user(user_id)
        all_searches = SearchHistory.get_all_previous_searches(self.request.user)
        if all_searches != None:
            data['searches'] = all_searches[::-1][:10]
        else:
            data['no_searches'] = True
        viewed_products = ProductViewed.get_all_viewed_products(self.request.user)
        data['products'] = viewed_products
        data['order_history'] = order_history_list
        return data

class UpdateProfile(TemplateView):
    template_name = 'update_profile.html'
    data = {}

    def post(self, request, *args, **kwargs):
        '''
        post
        this method allows the user to change information on the
        profile page then we redirect the user to the profile page
        '''
        if 'update_img' in request.POST:
            img = request.POST.get('update_img')
            Profile.update_img(img, request.user.id)
        if 'update_des' in request.POST:
            desc = request.POST.get('update_des')
            Profile.update_desc(desc, request.user.id)
        return redirect('profile')
