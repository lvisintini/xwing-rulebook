# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 02:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0015_auto_20161230_0249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reference',
            options={'ordering': ['source', 'page']},
        ),
    ]
