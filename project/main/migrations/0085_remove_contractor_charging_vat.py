# Generated by Django 2.2.27 on 2022-04-07 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0084_auto_20220407_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractor',
            name='charging_vat',
        ),
    ]
