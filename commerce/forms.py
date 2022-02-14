from django import forms
from .models import Address

payment_choices = [
    ('S', 'Stripe'),
    ('P', 'PayPal')
]


class CheckoutForm(forms.Form):
    # same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    # save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=payment_choices)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['post_code', 'main_address', 'detailed_address', 'mark_as']


class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['post_code', 'main_address', 'detailed_address', 'mark_as', 'default']
