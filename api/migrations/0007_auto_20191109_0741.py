# Generated by Django 2.2.7 on 2019-11-09 01:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20191109_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 9, 7, 41, 24, 864883)),
        ),
    ]