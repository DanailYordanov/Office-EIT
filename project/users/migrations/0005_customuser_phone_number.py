# Generated by Django 2.2.24 on 2022-01-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_debit_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Телефонен номер'),
        ),
    ]
