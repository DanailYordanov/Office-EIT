# Generated by Django 2.2.27 on 2022-03-20 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0073_auto_20220320_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triporder',
            name='course_export',
        ),
        migrations.RemoveField(
            model_name='triporder',
            name='course_import',
        ),
        migrations.AddField(
            model_name='triporder',
            name='course',
            field=models.OneToOneField(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='trip_order_course', to='main.Course', verbose_name='Курс за износ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='triporder',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip_order_creator', to=settings.AUTH_USER_MODEL, verbose_name='Създател'),
        ),
        migrations.AlterField(
            model_name='triporder',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip_order_driver', to=settings.AUTH_USER_MODEL, verbose_name='Шофьор'),
        ),
    ]