# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtre', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagina',
            name='nom',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
