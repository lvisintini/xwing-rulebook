# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-14 00:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0003_remove_source_version'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clausecontent',
            options={},
        ),
        migrations.RemoveField(
            model_name='clausecontent',
            name='active',
        ),
    ]
