# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-20 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0037_auto_20170520_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clause',
            name='group',
            field=models.IntegerField(choices=[(1, 'Main'), (2, 'Images'), (3, 'Card Errata'), (4, 'Card Clarification'), (5, 'Huge Ship Related')], default=1),
        ),
    ]
