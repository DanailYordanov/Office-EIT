# Generated by Django 2.2.24 on 2022-01-29 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_course_export'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseinvoice',
            name='measure_type',
        ),
        migrations.RemoveField(
            model_name='courseinvoice',
            name='price',
        ),
        migrations.RemoveField(
            model_name='courseinvoice',
            name='quantity',
        ),
    ]
