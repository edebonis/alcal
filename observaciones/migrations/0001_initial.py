# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0002_alumno_año'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('mensaje', models.CharField(max_length=500)),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
            ],
        ),
    ]
