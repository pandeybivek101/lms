# Generated by Django 2.1.7 on 2020-02-03 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_auto_20200201_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudentModel',
        ),
    ]
