# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('identificacao', '0013_auto_20151028_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enderecodetalhe',
            name='mostra_bayface',
            field=models.BooleanField(default=False, help_text='', verbose_name='Mostra no bayface'),
        ),
        migrations.AlterField(
            model_name='identificacao',
            name='historico',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 6, 12, 40, 41, 685772), verbose_name='Hist\xf3rico', editable=False),
        ),
    ]
