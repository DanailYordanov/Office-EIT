# Generated by Django 2.2.24 on 2022-01-26 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_taxtransactionbasis'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinvoice',
            name='tax_transaction_basis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.TaxTransactionBasis', verbose_name='Основане на сделка'),
        ),
    ]
