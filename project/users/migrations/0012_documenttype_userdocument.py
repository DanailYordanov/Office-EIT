# Generated by Django 2.2.27 on 2022-04-14 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20220414_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=100, verbose_name='Тип документ')),
            ],
        ),
        migrations.CreateModel(
            name='UserDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='user_files', verbose_name='Файл')),
                ('document_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.DocumentType', verbose_name='Тип документ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Потребител')),
            ],
        ),
    ]