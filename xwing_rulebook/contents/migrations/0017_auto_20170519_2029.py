# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0016_auto_20170511_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(blank=True, default='', max_length=125),
        ),
    ]
