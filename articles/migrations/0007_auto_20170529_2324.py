# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-29 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20170410_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='media',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='articles', verbose_name='Image'),
        ),
    ]
