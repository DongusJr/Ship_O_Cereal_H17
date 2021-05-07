from django import forms
from django.forms import ModelForm, widgets
from users.models import PersonInfo


class PersonInfoForm(ModelForm):
    class Meta:
        model = PersonInfo
        exclude = ['id']
        widgets = {
            'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'Street': widgets.TextInput(attrs={'class': 'form-control'}),
            'Country': widgets.Select(attrs={'class': 'form-control'}),
            'Zip': widgets.Select(attrs={'class': 'form-control'})
        }