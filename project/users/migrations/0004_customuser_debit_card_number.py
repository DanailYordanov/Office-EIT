# Generated by Django 2.2.24 on 2022-01-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211205_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='debit_card_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер на дебитна карта'),
        ),
    ]
