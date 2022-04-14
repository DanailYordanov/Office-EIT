# Generated by Django 2.2.27 on 2022-04-14 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20220408_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Bank', verbose_name='Банка'),
        ),
    ]
