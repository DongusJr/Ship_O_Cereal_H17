from django import forms
from django.forms import ModelForm, widgets

from cart.forms.creditcard_field import CreditCardField
from users.models import PaymentInfo


class PaymentForm(ModelForm):
    class Meta:
        model = PaymentInfo
        exclude = ['id']
        widgets = {
            'full_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'year': widgets.NumberInput(attrs={'class': 'form-control'}),
            'month': widgets.NumberInput(attrs={'class': 'form-control'}),
            'cvc': widgets.TextInput(attrs={'class': 'form-control'})
        }