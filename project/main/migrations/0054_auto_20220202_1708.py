# Generated by Django 2.2.24 on 2022-02-02 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_auto_20220201_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemedicalexamination',
            name='course',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_examination', to='main.Course', verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='courseserviceexamination',
            name='course',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_examination', to='main.Course', verbose_name='Курс'),
        ),
    ]
