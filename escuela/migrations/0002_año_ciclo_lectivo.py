# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='año',
            name='ciclo_lectivo',
            field=models.IntegerField(default=2015),
            preserve_default=False,
        ),
    ]
