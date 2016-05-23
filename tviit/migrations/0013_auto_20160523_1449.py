# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-23 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import tviit.models


class Migration(migrations.Migration):

    dependencies = [
        ('tviit', '0012_auto_20160523_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tviit',
            name='thumbnail',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=tviit.models.PathAndRename('attachments/thumbs')),
        ),
        migrations.AlterField(
            model_name='tviit',
            name='uuid',
            field=models.CharField(default=242646472987500404862674972859866880052L, editable=False, max_length=40, unique=True),
        ),
    ]