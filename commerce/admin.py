from django.contrib.admin import site
from .models import *

site.register(Profile)
site.register(Address)
