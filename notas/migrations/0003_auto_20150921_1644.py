# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0002_auto_20150921_1433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calificacionparcial',
            options={'verbose_name_plural': 'Calificaciones Parciales'},
        ),
        migrations.AlterModelOptions(
            name='calificaciontrimestral',
            options={'verbose_name_plural': 'Calificaciones Trimestrales'},
        ),
    ]
