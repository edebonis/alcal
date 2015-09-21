# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observaciones', '0004_auto_20150921_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='observacion',
            options={'verbose_name_plural': 'Observaciones'},
        ),
        migrations.AlterModelOptions(
            name='tipoobservacion',
            options={'verbose_name_plural': 'Tipos de Observaciones'},
        ),
    ]
