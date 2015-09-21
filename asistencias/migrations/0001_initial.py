# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0001_initial'),
        ('escuela', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateField()),
                ('alumno', smart_selects.db_fields.ChainedForeignKey(to='alumnos.Alumno', chained_field='año', auto_choose=True, chained_model_field='año')),
            ],
        ),
        migrations.CreateModel(
            name='CodigoAsistencia',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='asistencia',
            name='codigo',
            field=models.ForeignKey(to='asistencias.CodigoAsistencia'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='curso',
            field=models.ForeignKey(to='escuela.Curso'),
        ),
    ]
