# Generated by Django 2.2.7 on 2020-11-09 11:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='visit_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), blank=True, null=True, size=12),
        ),
    ]