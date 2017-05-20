# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-20 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0036_source_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clause',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('item:ul', 'Unordered Item'), ('item:ol', 'Ordered Item'), ('header', 'Header')], default='text', max_length=11),
        ),
    ]
