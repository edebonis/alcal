# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observaciones', '0003_auto_20150921_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='mensaje',
            field=models.TextField(max_length=500),
        ),
    ]
