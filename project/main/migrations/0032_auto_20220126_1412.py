# Generated by Django 2.2.24 on 2022-01-26 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20220125_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinvoice',
            name='quantity',
            field=models.FloatField(verbose_name='Количество'),
        ),
    ]
