from django.shortcuts import render
from django.views.generic import *
from .models import Item


class HomeLandingView(ListView):
    model = Item
    paginate_by = 10
    ordering = ['-id']
    template_name = 'core/item_list.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = ''
    query_pk_and_slug = True
    slug_field = 'item_slug'
    slug_url_kwarg = 'item_slug'


