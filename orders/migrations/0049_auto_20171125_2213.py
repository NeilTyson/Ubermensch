# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-25 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0048_inspectorreport_generated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectorreport',
            name='generated_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Profile'),
        ),
    ]