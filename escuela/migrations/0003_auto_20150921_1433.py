# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0002_año_ciclo_lectivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='curso',
            old_name='año',
            new_name='ciclo_lectivo',
        ),
        migrations.RemoveField(
            model_name='año',
            name='año',
        ),
    ]
