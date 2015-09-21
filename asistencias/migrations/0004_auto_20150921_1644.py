# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asistencias', '0003_auto_20150921_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codigoasistencia',
            options={'verbose_name_plural': 'Codigos de Asistencias'},
        ),
    ]
