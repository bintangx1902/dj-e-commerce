from django.urls import path
from .views import *

app_name = 'com'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/<slug:item_slug>', ItemDetailView.as_view(), name='item-detail'),
    path('add-to-cart/<slug:item_slug>', add_to_cart, name='add-to-cart'),
]
