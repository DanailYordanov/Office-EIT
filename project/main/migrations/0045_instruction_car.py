# Generated by Django 2.2.24 on 2022-01-30 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_auto_20220130_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Car', verbose_name='Автомобил'),
        ),
    ]