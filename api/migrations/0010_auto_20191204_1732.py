# Generated by Django 2.2.7 on 2019-12-04 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20191130_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 3, 17, 32, 25, 783807)),
        ),
    ]
