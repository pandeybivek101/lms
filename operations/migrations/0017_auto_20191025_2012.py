# Generated by Django 2.1.7 on 2019-10-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0016_auto_20191025_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addbooks',
            name='books_image',
            field=models.ImageField(upload_to='image'),
        ),
    ]
