# Generated by Django 2.2.27 on 2022-05-07 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0098_coursemedicalexamination_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetechnicalinspection',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_technical_inspection_driver', to=settings.AUTH_USER_MODEL, verbose_name='Шофьор'),
        ),
    ]
