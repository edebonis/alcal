# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoObservacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='observacion',
            name='tipo',
            field=models.ForeignKey(to='observaciones.TipoObservacion', default=''),
            preserve_default=False,
        ),
    ]
