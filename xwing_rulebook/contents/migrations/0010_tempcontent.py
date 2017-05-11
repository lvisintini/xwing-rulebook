# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-11 09:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0035_auto_20170510_2225'),
        ('contents', '0009_auto_20170509_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('text', 'Text'), ('image', 'Image')], default='text', max_length=5)),
                ('title', models.CharField(blank=True, max_length=125, null=True)),
                ('preserve_title_case', models.BooleanField(default=False)),
                ('page', models.IntegerField(blank=True, null=True)),
                ('content', models.TextField(default='')),
                ('content_as_per_source', models.TextField(blank=True, default='', help_text="If the text in the content field is not a verbatim copy of the source's text, Add the original text here.")),
                ('keep_line_breaks', models.BooleanField(default=False)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contents.Image')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rules.Source')),
            ],
        ),
    ]
