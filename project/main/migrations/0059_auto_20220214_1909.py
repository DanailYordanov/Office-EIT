# Generated by Django 2.2.27 on 2022-02-14 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_auto_20220214_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='FromTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_to', models.CharField(max_length=100, verbose_name='Релация')),
            ],
            options={
                'verbose_name': 'Релация',
                'verbose_name_plural': 'Релации',
            },
        ),
        migrations.AlterModelOptions(
            name='courseinvoice',
            options={'verbose_name': 'Фактура за курс', 'verbose_name_plural': 'Фактури за курсове'},
        ),
    ]
