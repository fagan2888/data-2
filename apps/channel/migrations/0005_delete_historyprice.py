# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0004_blockchainstats'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoryPrice',
        ),
    ]