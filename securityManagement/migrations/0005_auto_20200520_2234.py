# Generated by Django 2.2.11 on 2020-05-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securityManagement', '0004_auto_20200511_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='email',
            field=models.EmailField(error_messages={'unique': 'The email is already being used by a recipient.'}, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='register_num',
            field=models.IntegerField(unique=True),
        ),
    ]
