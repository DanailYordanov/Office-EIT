# Generated by Django 2.2.27 on 2022-04-07 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0082_requestnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='request_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.RequestNumber', verbose_name='Номер на заявка'),
        ),
    ]
