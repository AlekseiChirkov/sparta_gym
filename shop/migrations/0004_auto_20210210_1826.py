# Generated by Django 2.2.7 on 2021-02-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210210_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelist',
            name='description_1',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='description_2',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='description_3',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='description_4',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='description_5',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
