from django import forms

payment_choices = [
    ('S', 'Stripe'),
    ('P', 'PayPal')
]


class CheckoutForm(forms.Form):
    # same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    # save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=payment_choices)
