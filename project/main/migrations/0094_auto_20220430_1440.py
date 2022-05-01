# Generated by Django 2.2.27 on 2022-04-30 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0093_course_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triporder',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_order_course', to='main.Course', verbose_name='Курс за износ'),
        ),
    ]
