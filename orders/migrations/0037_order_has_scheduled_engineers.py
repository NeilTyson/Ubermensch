# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-20 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_contract_form_of_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='has_scheduled_engineers',
            field=models.BooleanField(default=False),
        ),
    ]
