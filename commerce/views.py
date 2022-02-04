from django.shortcuts import get_object_or_404, reverse, render, redirect
from django.views.generic import *
from core.models import Item, OrderItem, Order, BillingAddress, Payment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import stripe

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
                    zip_code=zip_code
                )
                bil_add.save()
                order.billing_address = bil_add
                order.save()

                return redirect('com:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an active order ! ")
            return redirect('com:order-summary')

        messages.warning(self.request, "Checkout Failed")
        return redirect('com:checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'com/payment.html')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.GET.get('stripeToken')
        amount = order.get_total()

        # error handling
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="idr",
                source=token,
            )

            order.ordered = True
            payment = Payment()
            payment.stripe_charge_id = charge.id
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            messages.success(self.request, " Your order was successful ! ")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.error(self.request, f'{e.user_message} - code : {e.code}')

            # print('Status is: %s' % e.http_status)
            # print('Code is: %s' % e.code)
            # param is '' in this case
            # print('Param is: %s' % e.param)
            # print('Message is: %s' % e.user_message)
        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Rate limit error ! ")

        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid Parameters")

        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Not Authenticated")

        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network error ")

        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong. You were not charged. Please try again later! ")

        except Exception as e:
            messages.error(self.request, "Serious error occurred. we have been notified")
        # end handling

        return redirect('/')




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
