from django import forms
from django.forms import ModelForm, widgets

from users.models import PaymentInfo


class PaymentForm(ModelForm):
    class Meta:
        '''
        this meta class allows to retain and make sure that the user
        inputs all information which is required to complete a payment process
        '''
        model = PaymentInfo
        exclude = ['id']
        widgets = {
            'full_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'year': widgets.NumberInput(attrs={'class': 'form-control'}),
            'month': widgets.NumberInput(attrs={'class': 'form-control'}),
            'cvc': widgets.TextInput(attrs={'class': 'form-control'})
        }