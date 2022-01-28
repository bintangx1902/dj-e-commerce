from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_counter(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            qs = qs.first()
            count = 0
            for quantity in qs.item.all():
                count += quantity.quantity
        return count
    return 0
