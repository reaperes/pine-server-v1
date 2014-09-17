import os

from django.db import migrations
from django.utils import timezone


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    user1 = apps.get_model('pine', 'Users').objects.get(id=1)
    user6 = apps.get_model('pine', 'Users').objects.get(id=6)
    thread3 = apps.get_model('pine', 'Threads').objects.get(id=3)
    comments = apps.get_model('pine', 'Comments')
    comments.objects.using(db_alias).bulk_create([
        comments(author=user1, thread=thread3, content='comment test', pub_date=timezone.now()),
        comments(author=user6, thread=thread3, content='com', pub_date=timezone.now())
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0004_auths'),
    ]

    operations = [
    ]

    if os.environ['DJANGO_SETTINGS_MODULE'] != 'PineServerProject.settings.production':
        operations.append(migrations.RunPython(
            forwards_func,
        ))