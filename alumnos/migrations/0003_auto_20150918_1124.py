# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0002_alumno_año'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre_tutor', models.CharField(max_length=50)),
                ('apellido_tutor', models.CharField(max_length=50)),
                ('dni_tutor', models.IntegerField(blank=True, null=True)),
                ('direccion_tutor', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono_tutor', models.CharField(max_length=20)),
                ('nacionalidad_tutor', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='alumno',
            name='tutor',
            field=models.ForeignKey(to='alumnos.Tutor', default=''),
            preserve_default=False,
        ),
    ]
