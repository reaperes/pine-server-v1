# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from pine.models import Phones, Auths

def forwards_func(apps, schema_editor):
    Phones = apps.get_model("pine", "Phones")
    p = Phones.objects.get(phone_number="01085174557")
    Auths = apps.get_model("pine", "Auths")
    db_alias = schema_editor.connection.alias
    Auths.objects.using(db_alias).bulk_create([
        Auths(phone=p, auth_number="111111")
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0002_load_fixtures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auths',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('auth_number', models.CharField(max_length=6)),
                ('phone', models.OneToOneField(to='pine.Phones')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            forwards_func,
        )
    ]
