# Generated by Django 2.2.27 on 2022-04-04 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_auto_20220327_0050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseaddress',
            old_name='address_obj',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='courseaddress',
            name='address_input',
        ),
    ]