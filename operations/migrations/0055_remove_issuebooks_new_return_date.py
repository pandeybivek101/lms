# Generated by Django 2.1.7 on 2019-12-29 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0054_issuebooks_renewed_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuebooks',
            name='new_return_date',
        ),
    ]
