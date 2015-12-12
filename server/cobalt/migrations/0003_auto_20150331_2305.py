# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from cobalt.util import string_to_url

def fix_genre_names(apps, schema_editor):
    Genre = apps.get_model("cobalt", "Genre")

    for genre in Genre.objects.all():
        genre.name = string_to_url(genre.name)
        genre.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cobalt', '0002_auto_20150328_1245'),
    ]

    operations = [
        migrations.RunPython(fix_genre_names),
    ]
