# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0001_initial'),
        ('escuela', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalificacionParcial',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nota', models.IntegerField()),
                ('fecha', models.DateField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
                ('materia', models.ForeignKey(to='escuela.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='CalificacionTrimestral',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nota', models.IntegerField()),
                ('alumno', models.ForeignKey(to='alumnos.Alumno')),
                ('materia', models.ForeignKey(to='escuela.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Trimestre',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('trimestre', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='calificaciontrimestral',
            name='trimestre',
            field=models.ForeignKey(to='notas.Trimestre'),
        ),
        migrations.AddField(
            model_name='calificacionparcial',
            name='trimestre',
            field=models.ForeignKey(to='notas.Trimestre'),
        ),
    ]
