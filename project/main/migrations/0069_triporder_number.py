# Generated by Django 2.2.27 on 2022-03-14 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0068_auto_20220314_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='triporder',
            name='number',
            field=models.IntegerField(default=1, verbose_name='№'),
            preserve_default=False,
        ),
    ]
