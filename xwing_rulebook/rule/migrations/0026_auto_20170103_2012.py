# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0025_remove_clause_clause_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksection',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
