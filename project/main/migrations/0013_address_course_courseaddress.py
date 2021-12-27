# Generated by Django 2.2.24 on 2021-12-24 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('contact_person', models.CharField(max_length=50, verbose_name='Лице за контакт')),
                ('contact_phone', models.CharField(max_length=30, verbose_name='Телефон за връзка')),
                ('gps_coordinats', models.CharField(max_length=100, verbose_name='GPS координати')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_to', models.CharField(max_length=100, verbose_name='Релация')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('currency', models.CharField(choices=[('BGN', 'BGN'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CAD', 'CAD')], max_length=5, verbose_name='Валута')),
                ('cargo_type', models.CharField(max_length=100, verbose_name='Вид и тегло на товара')),
                ('other_conditions', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Други условия')),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Bank', verbose_name='Банка')),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Car', verbose_name='Автомобил')),
                ('contractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Contractor', verbose_name='Контрагент')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Шофьор')),
            ],
        ),
        migrations.CreateModel(
            name='CourseAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loаding_type', models.CharField(choices=[('loading_address', 'Адрес на товарене'), ('unloading_address', 'Адрес на разтоварване')], max_length=20, verbose_name='Вид на товарене')),
                ('date', models.DateField(verbose_name='Дата')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Address', verbose_name='Адрес')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course', verbose_name='Курс')),
            ],
        ),
    ]