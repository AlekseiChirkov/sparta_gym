# Generated by Django 2.2.7 on 2019-11-09 01:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191109_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 9, 7, 32, 52, 946973)),
        ),
        migrations.DeleteModel(
            name='PaymentToProduct',
        ),
    ]