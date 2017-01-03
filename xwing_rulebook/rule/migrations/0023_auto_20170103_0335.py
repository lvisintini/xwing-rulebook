# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 03:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0022_auto_20170103_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClauseContentVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('clause', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rule.Clause')),
            ],
            options={
                'ordering': ['active'],
            },
        ),
        migrations.RemoveField(
            model_name='clausecontent',
            name='clause',
        ),
        migrations.AddField(
            model_name='clausecontentversion',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rule.ClauseContent'),
        ),
        migrations.AddField(
            model_name='clause',
            name='available_contents',
            field=models.ManyToManyField(through='rule.ClauseContentVersion', to='rule.ClauseContent'),
        ),
    ]
