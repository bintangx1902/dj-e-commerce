from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings
from os import remove, path


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    discount = models.FloatField()
    item_slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField(config_name='default',
                                verbose_name='Product Description ',
                                external_plugin_resources=[
                                    ('youtube',
                                     '/static/ckeditor_plugins/youtube/youtube/',
                                     'plugin.js')
                                ],
                                default='')
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return

    def delete(self, using=None, *args, **kwargs):
        remove(path.join(settings.MEDIA_ROOT, self.image.name))
        super().delete(*args, **kwargs)


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


models.signals.post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
