# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0003_auto_20150918_0032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='año',
        ),
        migrations.RemoveField(
            model_name='materia',
            name='carrera',
        ),
        migrations.AddField(
            model_name='materia',
            name='curso',
            field=models.ForeignKey(to='escuela.Curso', default=''),
            preserve_default=False,
        ),
    ]
