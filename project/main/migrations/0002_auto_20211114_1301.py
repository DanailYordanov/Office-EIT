# Generated by Django 2.2.24 on 2021-11-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.CharField(max_length=50, verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='car',
            name='number_plate',
            field=models.CharField(max_length=50, verbose_name='Регистрационен номер'),
        ),
    ]
