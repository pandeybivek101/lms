# Generated by Django 2.1.7 on 2019-10-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0020_auto_20191026_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebookrequesthistory',
            name='action_date',
            field=models.DateTimeField(),
        ),
    ]
