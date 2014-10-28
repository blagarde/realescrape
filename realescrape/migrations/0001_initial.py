# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=200)),
                ('price', models.FloatField()),
                ('size', models.FloatField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('postcode', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=15)),
                ('listed_on', models.CharField(max_length=15)),
                ('unread', models.BooleanField(default=True)),
                ('blacklisted', models.DateTimeField(null=True, blank=True)),
                ('star', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
