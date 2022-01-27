from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings
from os import remove, path
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=255, verbose_name='Nama Produk : ')
    price = models.FloatField(verbose_name="Harga Asli : ")
    discount = models.FloatField(verbose_name="Harga yang akan di jual : ", blank=True, null=True)
    item_slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField(config_name='default',
                                verbose_name='Deskripsi Produk : ',
                                external_plugin_resources=[
                                    ('youtube',
                                     '/static/ckeditor_plugins/youtube/youtube/',
                                     'plugin.js')
                                ],
                                default='')
    image = models.ImageField(upload_to='img/', verbose_name="Poto Terkait Produk : ")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return

    def get_absolute_url(self):
        return reverse('com:item-detail', kwargs={'item_slug': self.item_slug})

    def get_add_to_cart_url(self):
        return reverse('com:add-to-cart', kwargs={'item_slug': self.item_slug})

    def get_remove_from_cart_url(self):
        return reverse('com:remove-from-cart', kwargs={'item_slug': self.item_slug})

    def delete(self, using=None, *args, **kwargs):
        remove(path.join(settings.MEDIA_ROOT, self.image.name))
        super().delete(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


models.signals.post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
