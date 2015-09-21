# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('legajo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono', models.CharField(max_length=20)),
                ('nacionalidad', models.CharField(max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('libre', models.BooleanField(default=False)),
                ('condicional', models.BooleanField(default=False)),
                ('año', models.ForeignKey(to='escuela.Año')),
            ],
        ),
        migrations.CreateModel(
            name='Madre',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre_madre', models.CharField(max_length=50)),
                ('apellido_madre', models.CharField(max_length=50)),
                ('dni_madre', models.IntegerField(blank=True, null=True)),
                ('direccion_madre', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono_madre', models.CharField(max_length=20)),
                ('nacionalidad_madre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Padre',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre_padre', models.CharField(max_length=50)),
                ('apellido_padre', models.CharField(max_length=50)),
                ('dni_padre', models.IntegerField(blank=True, null=True)),
                ('direccion_padre', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono_padre', models.CharField(max_length=20)),
                ('nacionalidad_padre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre_tutor', models.CharField(max_length=50)),
                ('apellido_tutor', models.CharField(max_length=50)),
                ('dni_tutor', models.IntegerField(blank=True, null=True)),
                ('direccion_tutor', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono_tutor', models.CharField(max_length=20)),
                ('nacionalidad_tutor', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='alumno',
            name='madre',
            field=models.ForeignKey(to='alumnos.Madre', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='padre',
            field=models.ForeignKey(to='alumnos.Padre', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumno',
            name='tutor',
            field=models.ForeignKey(to='alumnos.Tutor', blank=True, null=True),
        ),
    ]
