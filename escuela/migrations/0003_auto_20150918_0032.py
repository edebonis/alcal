# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0002_auto_20150918_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('curso', models.CharField(max_length=5)),
            ],
        ),
        migrations.RenameField(
            model_name='año',
            old_name='anio',
            new_name='año',
        ),
        migrations.RenameField(
            model_name='materia',
            old_name='anio',
            new_name='año',
        ),
        migrations.AddField(
            model_name='curso',
            name='año',
            field=models.ForeignKey(to='escuela.Año'),
        ),
        migrations.AddField(
            model_name='curso',
            name='carrera',
            field=models.ForeignKey(to='escuela.Carrera'),
        ),
    ]
