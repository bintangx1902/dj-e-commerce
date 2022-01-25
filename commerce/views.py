from django.shortcuts import get_object_or_404, reverse
from django.views.generic import *
from core.models import Item, OrderItem, Order


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
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__item_slug=item.item_slug).exists():
            order_item.quantity += 1
            order_item.save()

    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)

    return reverse('com:item-detail', kwargs={'item_slug': item_slug})
