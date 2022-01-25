from django.shortcuts import get_object_or_404
from django.views.generic import *
from core.models import Item


class HomeView(ListView):
    model = Item
    template_name = 'com/home.html'
    paginate_by = 50
    ordering = ['-pk']
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = None
    query_pk_and_slug = True
    slug_field = 'item_slug'
    slug_url_kwarg = 'item_slug'


def add_to_cart(request, item_slug):
    item = get_object_or_404(Item, item_slug=item_slug)

