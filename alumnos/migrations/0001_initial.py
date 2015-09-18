# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('legajo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.IntegerField(null=True, blank=True)),
                ('direccion', models.CharField(null=True, blank=True, max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('nacionalidad', models.CharField(max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('libre', models.BooleanField(default=False)),
                ('condicional', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Madre',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre_madre', models.CharField(max_length=50)),
                ('apellido_madre', models.CharField(max_length=50)),
                ('dni_madre', models.IntegerField(null=True, blank=True)),
                ('direccion_madre', models.CharField(null=True, blank=True, max_length=100)),
                ('telefono_madre', models.CharField(max_length=20)),
                ('nacionalidad_madre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Padre',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre_padre', models.CharField(max_length=50)),
                ('apellido_padre', models.CharField(max_length=50)),
                ('dni_padre', models.IntegerField(null=True, blank=True)),
                ('direccion_padre', models.CharField(null=True, blank=True, max_length=100)),
                ('telefono_padre', models.CharField(max_length=20)),
                ('nacionalidad_padre', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='alumno',
            name='madre',
            field=models.ForeignKey(to='alumnos.Madre'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='padre',
            field=models.ForeignKey(to='alumnos.Padre'),
        ),
    ]
