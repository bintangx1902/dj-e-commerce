# Generated by Django 3.2.8 on 2022-02-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_coupon_disc_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='disc_amount',
            field=models.IntegerField(default=0, verbose_name='Discount in percent '),
        ),
    ]
