# Generated by Django 2.1.7 on 2019-11-08 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0042_auto_20191108_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
