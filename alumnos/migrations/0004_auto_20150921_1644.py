# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnos', '0003_alumno_curso'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tutor',
            options={'verbose_name_plural': 'Tutores'},
        ),
    ]
