# Generated by Django 2.2.24 on 2022-01-29 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_auto_20220128_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='export',
            field=models.BooleanField(default=False, verbose_name='За износ'),
        ),
    ]
