# Generated by Django 2.2.24 on 2021-12-27 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_course_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseaddress',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Address', verbose_name='Адрес'),
        ),
    ]
