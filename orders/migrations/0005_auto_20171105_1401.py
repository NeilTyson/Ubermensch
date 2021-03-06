# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20171105_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bir_certificate',
            field=models.ImageField(blank=True, default='na', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='dole_certification',
            field=models.ImageField(blank=True, default='na', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='org_chart',
            field=models.ImageField(blank=True, default='na', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='sec_registration_form',
            field=models.ImageField(blank=True, default='na', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='sss_certificate',
            field=models.ImageField(blank=True, default='na', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='vendor_application',
            field=models.ImageField(blank=True, default='na', upload_to=''),
            preserve_default=False,
        ),
    ]
