# Generated by Django 3.0.4 on 2020-04-18 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securityManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipient',
            name='register_num',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
