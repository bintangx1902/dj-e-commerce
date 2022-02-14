from django.urls import path
from .views import *

# TODO : we didnt need billing address anymore, we changed to address to save the payment and shipping 

app_name = 'com'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile', Profile.as_view(), name='profile'),
    path('profile/add-address', CreateAddressView.as_view(), name='create-address'),
    path('profile/update-address/<slug:address_link>', UpdateAddressView.as_view(), name='create-address'),
    path('order/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCoupon.as_view(), name='add-coupon'),
    path('payment/success', PaymentSuccess.as_view(), name='payment-success'),
    path('payment/cancel', PaymentCancel.as_view(), name='payment-cancel'),
    path('payment/<payment_method>', PaymentView.as_view(), name='payment'),
    path('payment/<payment_method>/session-create', CreateCheckoutSessionView.as_view(), name='create-payment-session'),
    path('item/<slug:item_slug>', ItemDetailView.as_view(), name='item-detail'),
    path('add-to-cart/<slug:item_slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:item_slug>', remove_from_cart, name='remove-from-cart'),
    path('reduce-from-cart/<slug:item_slug>', reduce_item, name='reduce-item'),
]
