# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0003_auto_20150921_1433'),
        ('observaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='observacion',
            name='ciclo_lectivo',
            field=models.ForeignKey(to='escuela.Año', default=''),
            preserve_default=False,
        ),
    ]
