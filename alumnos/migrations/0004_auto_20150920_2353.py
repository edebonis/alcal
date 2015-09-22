# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0003_auto_20150918_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='madre',
            field=models.ForeignKey(blank=True, to='alumnos.Madre', null=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='padre',
            field=models.ForeignKey(blank=True, to='alumnos.Padre', null=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='tutor',
            field=models.ForeignKey(blank=True, to='alumnos.Tutor', null=True),
        ),
    ]
