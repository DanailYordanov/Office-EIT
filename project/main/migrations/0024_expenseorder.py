# Generated by Django 2.2.24 on 2022-01-08 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_triporder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BGN_amount', models.FloatField(verbose_name='Сума в лева')),
                ('EUR_amount', models.FloatField(verbose_name='Сума в евро')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Дата на създаване')),
                ('trip_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.TripOrder', verbose_name='Командировъчна заповед')),
            ],
        ),
    ]
