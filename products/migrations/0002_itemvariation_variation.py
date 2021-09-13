# Generated by Django 3.0.6 on 2021-08-21 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='products.Item', verbose_name='Item')),
            ],
            options={
                'verbose_name': 'Variation',
                'verbose_name_plural': 'Variations',
            },
        ),
        migrations.CreateModel(
            name='ItemVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_variations', to='products.Variation', verbose_name='Variation')),
            ],
            options={
                'verbose_name': 'Item Variation',
                'verbose_name_plural': 'Item Variations',
            },
        ),
    ]
