from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeLandingView.as_view(), name='home'),
    path('create-item', CreateItemViews.as_view(), name='item-create'),
    path('<slug:item_slug>', ItemDetailView.as_view(), name='item-detail'),
]
