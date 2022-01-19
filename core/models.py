from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    discount = models.FloatField()
    item_slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField
    image = models.ImageField(upload_to='img/')

