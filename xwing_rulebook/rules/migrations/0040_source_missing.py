# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-16 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0039_auto_20170608_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='missing',
            field=models.BooleanField(default=True),
        ),
    ]
