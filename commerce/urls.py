from django.urls import path
from .views import HomeView, ItemDetailView

app_name = 'com'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:item_slug>', ItemDetailView.as_view(), name='detail'),
]
