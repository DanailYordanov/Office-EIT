# Generated by Django 2.2.24 on 2022-01-26 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_course_request_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxTransactionBasis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Име')),
            ],
        ),
    ]
