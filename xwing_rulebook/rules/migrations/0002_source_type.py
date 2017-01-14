# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-13 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='type',
            field=models.CharField(choices=[('M', 'Manual'), ('RC', 'Reference Card'), ('RR', 'Rules Reference'), ('FAQ', 'FAQ')], default='RC', max_length=50),
        ),
    ]
