# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-04 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20171102_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='deadline_time',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='deadline_date',
            field=models.DateTimeField(),
        ),
    ]