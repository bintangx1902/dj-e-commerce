from django.shortcuts import get_object_or_404, reverse
from django.views.generic import *
from core.models import Item, OrderItem, Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages


class HomeView(ListView):
    model = Item
    template_name = 'com/home.html'
    paginate_by = 50
    ordering = ['-pk']
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'com/item.html'
    query_pk_and_slug = True
    slug_field = 'item_slug'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item'


@login_required(login_url='/accounts/login/')
def add_to_cart(request, item_slug):
    item = get_object_or_404(Item, item_slug=item_slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.item.filter(item__item_slug=item.item_slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item Quantity is updated")
        else:
            messages.info(request, "This item was added to your cart")
            order.item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, "This item was added to your cart")

    return HttpResponseRedirect(reverse('com:item-detail', kwargs={'item_slug': item_slug}))


def remove_from_cart(request, item_slug):
    item = get_object_or_404(Item, item_slug=item_slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.item.filter(item__item_slug=item.item_slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)
            order.item.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You dont have an active order")

    return HttpResponseRedirect(reverse('com:item-detail', kwargs={'item_slug': item_slug}))
