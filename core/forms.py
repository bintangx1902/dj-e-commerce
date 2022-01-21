from django import forms
from .models import *


class CreateItemForms(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
