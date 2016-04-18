# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tviit', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tviit',
            options={'ordering': ('created',)},
        ),
        migrations.AlterField(
            model_name='tviit',
            name='content',
            field=models.TextField(max_length=160),
        ),
        migrations.AlterField(
            model_name='tviit',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tviit.Tviit'),
        ),
    ]
