from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('cart', login_required(views.CartView.as_view()), name='cart_page'),
    path('cart/payment', login_required(views.CompletePurchase.as_view()), name='complete_order')
]