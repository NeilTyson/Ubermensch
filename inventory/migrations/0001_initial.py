# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 08:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0006_remove_product_reorder_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestedSupplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=5)),
                ('is_done', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Supplier')),
            ],
        ),
    ]
