# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtre', '0005_noticia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cataleg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('frases', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('path', models.CharField(max_length=200)),
                ('horari', models.TimeField(verbose_name="Hora d'actualització")),
            ],
        ),
        migrations.AlterField(
            model_name='noticia',
            name='font',
            field=models.ForeignKey(to='filtre.Font'),
        ),
        migrations.DeleteModel(
            name='Pagina',
        ),
        migrations.AddField(
            model_name='cataleg',
            name='fonts',
            field=models.ManyToManyField(to='filtre.Font'),
        ),
    ]
