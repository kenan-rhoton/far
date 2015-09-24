# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtre', '0002_pagina_nom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frase',
            name='pagina',
        ),
        migrations.AddField(
            model_name='frase',
            name='pagina',
            field=models.ForeignKey(default='1', to='filtre.Pagina'),
            preserve_default=False,
        ),
    ]
