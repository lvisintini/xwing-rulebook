# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-06 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0033_auto_20170504_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='additional_keywords',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
