# Generated by Django 2.1.7 on 2019-10-31 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0040_issuebooks_retured_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issuebooks',
            old_name='retured_date',
            new_name='returned_date',
        ),
        migrations.AddField(
            model_name='issuebooks',
            name='returned',
            field=models.BooleanField(default=0),
        ),
    ]
