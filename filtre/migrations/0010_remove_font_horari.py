# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-21 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtre', '0009_auto_20160620_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='font',
            name='horari',
        ),
    ]
