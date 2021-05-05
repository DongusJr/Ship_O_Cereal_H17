from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from users.models import Account, Order, OrderProduct

# Create your views here.

def login_register(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            print("LOGIN")
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print("IM LOGGED IN")
                return redirect('product_index')
            else:
                messages.error("wrong username and password")
        elif request.POST.get('submit') == 'register':
            print("REGISTER")
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                form.save()
            return redirect('landing_page')
    return render(request, 'proto_users/account.html', {
        'form_1' : UserCreationForm(),
        'form_2' : AuthenticationForm()
    })


# Create your views here.
class Profile(TemplateView):
    template_name = 'proto_account/proto_order.html'

    def get_context_data(self, **kwargs):
        data = super(Profile, self).get_context_data(**kwargs)
        user = self.request.user
        data['user'] = self.request.user
        data['previous_order'] = order
        previous_order = Order.objects.get(prev=order)
        dic = {}
        for order in previous_order:
            dic[order] = OrderProduct.objects.get(order=order)
        data['order'] = dic
        return data
