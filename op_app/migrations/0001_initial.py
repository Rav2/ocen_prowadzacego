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
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('wisdom', models.IntegerField()),
                ('teaching', models.IntegerField()),
                ('friendliness', models.IntegerField()),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='LecturerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('info', models.CharField(max_length=2000)),
            ],
            options={
                'db_table': 'LecturerProfile',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='WorkPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('town', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'WorkPlace',
            },
        ),
        migrations.AddField(
            model_name='lecturerprofile',
            name='tags',
            field=models.ManyToManyField(db_table='LecturerTags', to='op_app.Tags'),
        ),
        migrations.AddField(
            model_name='lecturerprofile',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lecturerprofile',
            name='work_places',
            field=models.ManyToManyField(db_table='LecturerWorkPlace', to='op_app.WorkPlace'),
        ),
        migrations.AddField(
            model_name='comment',
            name='profile_id',
            field=models.ForeignKey(to='op_app.LecturerProfile'),
        ),
    ]
