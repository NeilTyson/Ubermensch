# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 08:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20171105_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='had_canvassed_suppliers',
        ),
    ]