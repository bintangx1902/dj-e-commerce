# Generated by Django 3.2.8 on 2022-02-11 17:26

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_billingaddress_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
