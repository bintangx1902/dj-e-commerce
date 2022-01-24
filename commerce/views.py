from django.shortcuts import render
from django.views.generic import *
from core.models import Item

item_slug = 'item_slug'


class HomeView(ListView):
    model = Item
    template_name = None
    paginate_by = 50
    ordering = ['-pk']


class ItemDetailView(DetailView):
    model = Item
    template_name = None
    query_pk_and_slug = True
    slug_field = item_slug
    slug_url_kwarg = item_slug


