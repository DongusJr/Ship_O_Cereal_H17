from django import forms
from django.forms import ModelForm, widgets
from users.models import PersonInfo


class PersonInfoForm(ModelForm):
    class Meta:
        '''
        this meta class allows to retain and make sure that the user
        inputs all information which is required to complete a payment process
        '''
        model = PersonInfo
        exclude = ['id']
        widgets = {
            'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'Street': widgets.TextInput(attrs={'class': 'form-control'}),
            'Country': widgets.Select(attrs={'class': 'form-control'}),
            'city_name': widgets.TextInput(attrs={'class': 'forms-control'}),
            'zip': widgets.TextInput(attrs={'class': 'form-control'}),
        }