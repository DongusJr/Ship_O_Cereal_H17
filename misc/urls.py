from django.urls import path
from . import views

urlpatterns = [
    path('', views.AboutUs.as_view(), name='misc'),
    path('', views.EmailNewsLetter.as_view(), name='email_news')
]