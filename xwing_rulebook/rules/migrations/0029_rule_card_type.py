# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0028_auto_20170416_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='card_type',
            field=models.IntegerField(blank=True, choices=[(0, 'N/A'), (1, 'Pilot'), (3, 'Condition'), (4, 'Damage card (Original core set)'), (5, 'Damage card (TFA core set)')], default=0),
        ),
    ]
