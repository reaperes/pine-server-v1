import os

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    phones = apps.get_model("pine", "Phones")
    p = phones.objects.get(phone_number="01085174557")
    auths = apps.get_model("pine", "Auths")
    db_alias = schema_editor.connection.alias
    auths.objects.using(db_alias).bulk_create([
        auths(phone=p, auth_number="111111")
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0003_auto_20140904_1602'),
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
    ]

    if os.environ['DJANGO_SETTINGS_MODULE'] != 'PineServerProject.settings.production':
        operations.append(migrations.RunPython(
            forwards_func,
        ))