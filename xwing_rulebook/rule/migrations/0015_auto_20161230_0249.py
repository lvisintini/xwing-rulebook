# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0014_paragraph_needs_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='code',
            field=models.CharField(default='', max_length=25, unique=True),
        ),
    ]
