# Generated by Django 2.1.7 on 2020-02-01 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0057_auto_20200201_1337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='catagory',
            old_name='added_by',
            new_name='catagory_added_by',
        ),
    ]
