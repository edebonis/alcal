# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observacion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('mensaje', models.CharField(max_length=500)),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='TipoObservacion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='observacion',
            name='tipo',
            field=models.ForeignKey(to='observaciones.TipoObservacion'),
        ),
    ]
