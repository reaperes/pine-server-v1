# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Phones = apps.get_model("pine", "Phones")
    Phones.objects.using(db_alias).bulk_create([
        Phones(phone_number="01032080403"),
        Phones(phone_number="01098590530"),
        Phones(phone_number="01087537711"),
        Phones(phone_number="01021101783"),
        Phones(phone_number="01040099179"),
        Phones(phone_number="01089607165"),
        Phones(phone_number="01037585989"),
        Phones(phone_number="01020624493"),
        Phones(phone_number="01020863441"),
        Phones(phone_number="01085174557"),
        Phones(phone_number="01026969960")
    ])

    Auths = apps.get_model("pine", "Auths")
    Auths.objects.using(db_alias).bulk_create([
        Auths(phone=Phones.objects.get(phone_number="01085174557"), auth_number="111111"),
    ])

    Users = apps.get_model("pine", "Users")
    Users.objects.using(db_alias).bulk_create([

    ])

class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auths',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
