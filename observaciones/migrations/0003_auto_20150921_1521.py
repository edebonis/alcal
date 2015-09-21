# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0004_remove_curso_ciclo_lectivo'),
        ('observaciones', '0002_observacion_ciclo_lectivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='observacion',
            name='curso',
            field=models.ForeignKey(to='escuela.Curso', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='observacion',
            name='alumno',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='curso', to='alumnos.Alumno', auto_choose=True, chained_model_field='curso'),
        ),
    ]
