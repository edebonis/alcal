# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0003_auto_20150921_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='ciclo_lectivo',
        ),
    ]
