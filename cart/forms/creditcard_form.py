from django import forms
from cart.forms.creditcard_field import CreditCardField
from users.models import PaymentInfo


class PaymentForm(forms.Form):
    cc = CreditCardField()
    comment = forms.CharField()
