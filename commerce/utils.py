from .models import Address
import string, random


def user_address_check(request):
    user = request.user
    address = Address.objects.filter(user=user)
    if address.exists():
        for add in address:
            if add.default:
                return True
    return False


def address_link_generator():
    num = '1234567890'
    letter = string.ascii_letters
    raw = letter + num
    return ''.join(random.sample(raw, 16))
