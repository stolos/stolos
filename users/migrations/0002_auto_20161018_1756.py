# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-18 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sshpublickey',
            name='public_key',
            field=models.TextField(unique=True, validators=[users.models._validate_public_key]),
        ),
    ]
