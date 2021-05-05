from django.contrib.auth.views import LogoutView
from django.urls import path
from users import views

urlpatterns = [
    path('account', views.login_register, name='login_register'),
    path('logout', LogoutView.as_view(next_page='login_register'), name='logout'),
    path('profile', views.Profile.as_view(), name='profile')
]