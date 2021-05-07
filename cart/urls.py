from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.CartView.as_view(), name='cart_page'),
    path('cart', views.CartItems.as_view(), name='cart_items')
]