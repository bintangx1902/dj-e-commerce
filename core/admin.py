from django.contrib.admin import site
from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


site.register(Item)
site.register(UserProfile)
site.register(OrderItem)
site.register(Order)
site.register(Coupon)
