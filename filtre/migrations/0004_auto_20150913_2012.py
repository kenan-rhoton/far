# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtre', '0003_auto_20150913_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frase',
            name='pagina',
        ),
        migrations.AddField(
            model_name='pagina',
            name='frases',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Frase',
        ),
    ]
