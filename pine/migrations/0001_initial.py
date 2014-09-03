# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('max_like', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField()),
                ('content', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['pub_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phones',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(unique=True, max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Threads',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField()),
                ('max_like', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField()),
                ('image_url', models.CharField(default='', max_length=256)),
                ('content', models.CharField(max_length=1000)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(default='none', max_length=10)),
                ('push_id', models.CharField(null=True, max_length=255)),
                ('account', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('blocks', models.ManyToManyField(related_name='blocked', to='pine.Users')),
                ('followings', models.ManyToManyField(related_name='followers', to='pine.Users')),
                ('friend_phones', models.ManyToManyField(related_name='related_phone_user', to='pine.Phones')),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='pine.Users')),
                ('phone', models.OneToOneField(to='pine.Phones')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='threads',
            name='author',
            field=models.ForeignKey(related_name='authorized', to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='threads',
            name='likes',
            field=models.ManyToManyField(related_name='likeThreads', to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='threads',
            name='readers',
            field=models.ManyToManyField(related_name='readable', to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='threads',
            name='reports',
            field=models.ManyToManyField(related_name='reportThreads', to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.ManyToManyField(related_name='likeComments', to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='reports',
            field=models.ManyToManyField(related_name='reportComments', to='pine.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='thread',
            field=models.ForeignKey(to='pine.Threads'),
            preserve_default=True,
        ),
    ]
