from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from users import views

urlpatterns = [
    path('account', views.login_register, name='login_register'),
    path('logout', LogoutView.as_view(next_page='login_register'), name='logout'),
    path('profile', login_required(views.UserProfile.as_view()), name='profile'),
    path('update', login_required(views.UpdateProfile.as_view()), name='update_profile')
]