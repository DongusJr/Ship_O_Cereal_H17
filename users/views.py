from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect


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