# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0002_alumno_año'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('cantidad', models.IntegerField()),
                ('codigo', models.CharField(max_length=5)),
                ('fecha', models.DateField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
            ],
        ),
    ]
