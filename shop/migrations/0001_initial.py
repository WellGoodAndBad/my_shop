# Generated by Django 3.1.3 on 2020-11-11 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.IntegerField()),
                ('name_item', models.TextField(blank=True, max_length=1000)),
                ('purchase_price', models.FloatField(blank=True, max_length=250)),
                ('shop_price', models.FloatField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(blank=True, related_name='items', to='shop.ItemShop')),
            ],
        ),
    ]