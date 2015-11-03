# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cataleg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=200)),
                ('frases', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('path', models.CharField(max_length=200)),
                ('horari', models.TimeField(verbose_name="Hora d'actualització")),
                ('haserror', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('titol', models.CharField(max_length=200)),
                ('data', models.DateTimeField(verbose_name='Data de publicació')),
                ('font', models.ForeignKey(to='filtre.Font')),
            ],
        ),
        migrations.AddField(
            model_name='cataleg',
            name='fonts',
            field=models.ManyToManyField(to='filtre.Font'),
        ),
    ]
