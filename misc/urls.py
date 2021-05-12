from django.urls import path
from . import views

urlpatterns = [
    path('', views.AboutUs.as_view(), name='misc'),
    path('newsletter', views.EmailNewsLetter.as_view(), name='email_news')
]