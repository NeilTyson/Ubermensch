# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 15:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0065_auto_20171127_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryreceipt',
            name='date_created',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
