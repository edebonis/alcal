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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('legajo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.IntegerField(null=True, blank=True)),
                ('direccion', models.CharField(null=True, blank=True, max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('nacionalidad', models.CharField(max_length=20)),
                ('materia', models.ManyToManyField(to='escuela.Materia')),
            ],
        ),
    ]
