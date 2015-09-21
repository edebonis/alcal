# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('legajo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(max_length=100, null=True, blank=True)),
                ('telefono', models.CharField(max_length=20)),
                ('nacionalidad', models.CharField(max_length=20)),
                ('materia', models.ManyToManyField(to='escuela.Materia')),
            ],
        ),
    ]
