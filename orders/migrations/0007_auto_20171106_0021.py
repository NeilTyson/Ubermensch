# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 16:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_had_canvassed_suppliers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_under_maintenance',
            new_name='is_maintained',
        ),
    ]