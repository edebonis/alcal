# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0001_initial'),
        ('alumnos', '0002_remove_alumno_año'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='curso',
            field=models.ForeignKey(default='', to='escuela.Curso'),
            preserve_default=False,
        ),
    ]
