# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 17:45
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0006_rule_expansion_rule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paragraph',
            name='level',
        ),
        migrations.AddField(
            model_name='paragraph',
            name='format',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'level': 0, 'type': 'text'}),
        ),
    ]
