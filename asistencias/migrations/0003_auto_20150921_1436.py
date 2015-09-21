# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('asistencias', '0002_asistencia_ciclo_lectivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='alumno',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='curso', chained_model_field='curso', to='alumnos.Alumno', auto_choose=True),
        ),
    ]
