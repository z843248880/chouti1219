# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('pwd', models.CharField(max_length=30)),
            ],
        ),
    ]