# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('calificaciones', '0009_auto_20151126_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificaciontrimestral',
            name='alumno',
            field=smart_selects.db_fields.ChainedForeignKey(to='alumnos.Alumno', chained_field='curso', chained_model_field='curso'),
        ),
    ]
