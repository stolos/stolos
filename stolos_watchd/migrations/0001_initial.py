# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 17:03
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRoutingConfig',
            fields=[
                ('project_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, max_length=30)),
                ('domain', models.CharField(max_length=256)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]