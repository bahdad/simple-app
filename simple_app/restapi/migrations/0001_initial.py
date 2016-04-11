# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import simple_app.utils


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', simple_app.utils.SecureUrlField(max_length=255)),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
    ]
