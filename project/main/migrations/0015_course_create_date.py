# Generated by Django 2.2.24 on 2021-12-27 11:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20211227_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата на създаване'),
            preserve_default=False,
        ),
    ]