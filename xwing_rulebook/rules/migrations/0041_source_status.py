# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-20 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0040_source_missing'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='status',
            field=models.IntegerField(choices=[(1, 'Processed'), (2, 'Pending'), (3, 'Missing source')], default=3),
        ),
    ]
