# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20170403_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_answered',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Article'),
        ),
    ]
