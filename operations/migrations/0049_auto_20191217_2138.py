# Generated by Django 2.1.7 on 2019-12-17 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0048_auto_20191210_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebooks',
            name='book',
            field=models.FileField(upload_to='files'),
        ),
    ]
