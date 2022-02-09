from django.shortcuts import get_object_or_404, reverse, render, redirect
from django.views.generic import *
from core.models import Item, OrderItem, Order, BillingAddress, Payment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .forms import CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import stripe
from django.core.exceptions import ObjectDoesNotExist

stripe.api_key = settings.STRIPE_SECRET_KEY


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


class CheckoutView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'com/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                bil_add = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip_code
                )
                bil_add.save()
                order.billing_address = bil_add
                order.save()

                if payment_option == 'S':
                    return HttpResponseRedirect(reverse('com:payment', args=['Stripe']))
                elif payment_option == 'P':
                    return HttpResponseRedirect(reverse('com:payment', kwargs={'payment_method': "PayPal"}))
                else:
                    messages.warning(self.request, "Invalid payment options ")

        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an active order ! ")
            return redirect('com:order-summary')

        messages.warning(self.request, "Checkout Failed")
        return redirect('com:checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'com/payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total())



        return redirect('/')


class CreateCheckoutSessionView(View):
    def post(self, *args, **kwargs):
        host = self.request.get_host()
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total())
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency': 'idr',
                        'unit_amount': amount * 100,  # amount * usd_cents,
                        'product_data': {
                            'name': f"Billing for ",
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"http://{host}{reverse('com:payment-success')}",
            cancel_url=f"http://{host}{reverse('com:payment-cancel')}",
        )
        return redirect(checkout_session.url, code=303)


class PaymentSuccess(View):
    template_name = 'com/pay/success.html'
    def get(self, *args, **kwargs):
        return render(self.request, template_name)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()


class PaymentCancel(TemplateView):
    template_name = 'com/pay/cancel.html'


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
