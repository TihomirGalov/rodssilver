# Generated by Django 3.0.6 on 2021-09-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210901_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='contact',
            field=models.CharField(default='asasas', max_length=100, verbose_name='Contact'),
            preserve_default=False,
        ),
    ]
