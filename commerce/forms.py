from django import forms
from django_countries.fields import CountryField

payment_choices = [
    ('S', 'Stripe'),
    ('P', 'PayPal')
]


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Jl. Sudirman no 1'
    }))
    apartment_address = forms.CharField(required=False)
    country = CountryField(blank_label='(select country)').formfield()
    zip_code = forms.CharField()
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=payment_choices)
