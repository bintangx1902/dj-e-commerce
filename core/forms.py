from django import forms
from .models import *


class CreateItemForms(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'discount', 'description', 'image']

        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'})
        }


class UpdateItemForms(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'discount', 'description', 'image']
