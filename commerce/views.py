from django.shortcuts import get_object_or_404, reverse, render
from django.views.generic import *
from core.models import Item, OrderItem, Order
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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


class OrderSummaryView(ListView):
    model = Order
    template_name = 'com/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Order.objects.get(user=self.request.user, ordered=False)

    @method_decorator(login_required(login_url='accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderSummaryView, self).dispatch(request, *args, **kwargs)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form here
        return render(self.request, 'com/checkout.html' )


@login_required(login_url='/accounts/login/')
def add_to_cart(request, item_slug):
    link = request.GET.get('url')

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

    if link:
        return HttpResponseRedirect(redirect_to=link)
    return HttpResponseRedirect(reverse('com:item-detail', kwargs={'item_slug': item_slug}))


@login_required(login_url='accounts/login/')
def remove_from_cart(request, item_slug):
    url = request.GET.get('url')
    item = get_object_or_404(Item, item_slug=item_slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.item.filter(item__item_slug=item.item_slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False).first()
            order.item.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You dont have an active order")

    if url is not None:
        return HttpResponseRedirect(redirect_to=url)
    return HttpResponseRedirect(reverse('com:item-detail', kwargs={'item_slug': item_slug}))


def reduce_item(request, item_slug):
    url = request.GET.get('url')
    item = get_object_or_404(Item, item_slug=item_slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.item.filter(item__item_slug=item.item_slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False).first()
            if order_item.quantity == 1:
                return reverse('com:remove-from-cart', kwargs={'item_slug': item_slug})
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "This item was reduce from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You dont have an active order")

    if url is not None:
        return HttpResponseRedirect(redirect_to=url)
    return HttpResponseRedirect(reverse('com:item-detail', kwargs={'item_slug': item_slug}))

