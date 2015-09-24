# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Frase',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text_frase', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('url', models.URLField()),
                ('path', models.CharField(max_length=200)),
                ('horari', models.TimeField(verbose_name="Hora d'actualització")),
            ],
        ),
        migrations.AddField(
            model_name='frase',
            name='pagina',
            field=models.ManyToManyField(to='filtre.Pagina'),
        ),
    ]
