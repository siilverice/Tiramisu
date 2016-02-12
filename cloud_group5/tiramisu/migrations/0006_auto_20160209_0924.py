# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiramisu', '0005_auto_20160208_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cube',
            name='app_type',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='cost_max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='cost_min',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='iops',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='iops_max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='iops_min',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='latency',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='latency_max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='latency_min',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='percentc',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='percenti',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cube',
            name='percentl',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='app_type',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='cost_max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='iops',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='iops_min',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='latency',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='latency_max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='percentc',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='percenti',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requirements',
            name='percentl',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='state',
            name='iops',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='state',
            name='iops_hdd',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='state',
            name='iops_ssd',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='state',
            name='latency',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='state',
            name='latency_hdd',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='state',
            name='latency_ssd',
            field=models.FloatField(),
        ),
    ]
