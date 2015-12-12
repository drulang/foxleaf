# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobalt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='devart_url',
            field=models.CharField(max_length=200, unique=True, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='devart_profile_url',
            field=models.CharField(max_length=200, unique=True, blank=True, null=True),
            preserve_default=True,
        ),
    ]
