from django.urls import path
from .views import *

app_name = 'com'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('order/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('item/<slug:item_slug>', ItemDetailView.as_view(), name='item-detail'),
    path('add-to-cart/<slug:item_slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:item_slug>', remove_from_cart, name='remove-from-cart'),
    path('reduce-from-cart/<slug:item_slug>', reduce_item, name='reduce-item'),
]
