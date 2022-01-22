from .views import *
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', HomeLandingView.as_view(), name='home'),
    path('create-item', CreateItemViews.as_view(), name='item-create'),
    path('<slug:item_slug>/update', UpdateItemViews.as_view(), name='item-update'),
    path('<slug:item_slug>/delete', ItemDeleteView.as_view(), name='item-delete'),
    path('<slug:item_slug>', ItemDetailView.as_view(), name='item-detail'),
]
