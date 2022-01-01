# Generated by Django 2.2.24 on 2021-12-30 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20211230_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_type', models.CharField(max_length=50, verbose_name='Вид разход')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('currency', models.CharField(choices=[('', 'Избери'), ('BGN', 'BGN'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('CAD', 'CAD')], max_length=5, verbose_name='Валута')),
                ('payment_type', models.CharField(choices=[('', 'Избери'), ('Кеш', 'Кеш'), ('Дебитна карта', 'Дебитна карта'), ('Кредитна карта', 'Кредитна карта'), ('Банков превод', 'Банков превод')], max_length=50, verbose_name='Вид плащане')),
                ('additional_information', models.CharField(blank=True, max_length=500, null=True, verbose_name='Допълнителна информация')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course', verbose_name='Курс')),
                ('expense_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ExpenseType', verbose_name='Вид курс')),
            ],
        ),
    ]
