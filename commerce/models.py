from django.db import models
from django.contrib.auth.models import User
from core.models import Item
from ckeditor.fields import RichTextField

mark = [
    ('R', 'Rumah'),
    ('K', "Kantor")
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile/img/')

    def __str__(self):
        return f"{self.user} profile's"


class ItemComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = RichTextField(config_name='default')
    hide_username = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} comment @ {self.item}"


class Address(models.Model):
    post_code = models.CharField(max_length=255)
    address_link = models.SlugField(default='', max_length=255)
    main_address = models.TextField()
    detailed_address = models.CharField(max_length=255)
    mark_as = models.CharField(default='R', max_length=10, choices=mark)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    def __str__(self):
        if self.default:
            return f"{self.user}'s main address"
        return f"{self.user}'s address "
