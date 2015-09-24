# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtre', '0004_auto_20150913_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('titol', models.CharField(max_length=200)),
                ('data', models.DateTimeField(verbose_name='Data de publicació')),
                ('font', models.ForeignKey(to='filtre.Pagina')),
            ],
        ),
    ]
