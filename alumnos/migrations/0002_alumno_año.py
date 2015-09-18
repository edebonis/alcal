# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0002_auto_20150918_0027'),
        ('alumnos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='año',
            field=models.ForeignKey(default='', to='escuela.Año'),
            preserve_default=False,
        ),
    ]
