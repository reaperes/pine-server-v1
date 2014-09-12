# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0002_load_fixtures'),
    ]

    operations = [
        migrations.AddField(
            model_name='threads',
            name='views',
            field=models.ManyToManyField(to='pine.Users', related_name='viewThreads'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='threads',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
