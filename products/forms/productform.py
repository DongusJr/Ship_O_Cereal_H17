from django.forms import ModelForm, widgets
from django import forms

from products.models import Products, ProductTag



# class ProductCreateForm(ModelForm):
#     image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     energy = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     sugar = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     fat = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     saturates = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     serving_amount = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ProductTag.objects.all().values_list())
#     class Meta:
#         model = Products
#         exclude = ['id', 'nutritional_info']
#         widgets = {
#             'name': widgets.TextInput(attrs={'class': 'form-control'}),
#             'short_description': widgets.TextInput(attrs={'class': 'form-control'}),
#             'description': widgets.TextInput(attrs={'class': 'form-control'}),
#             'category': widgets.TextInput(attrs={'class': 'form-control'}),
#             'in_stock': widgets.NumberInput(attrs={'class': 'form-control'}),
#         }

class ProductCreateForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    in_stock = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    energy = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sugar = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fat = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    saturates = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    serving_amount = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ProductTag.objects.all().values_list())

class ProductUpdateForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    in_stock = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    energy = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sugar = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fat = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    saturates = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    serving_amount = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ProductTag.objects.all().values_list())
