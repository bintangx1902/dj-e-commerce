from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeLandingView.as_view(), name='home'),
    path('<slug:item_slug>', ItemDetailView.as_view(), name='item-detail'),
]
