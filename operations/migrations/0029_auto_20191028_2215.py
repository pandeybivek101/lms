# Generated by Django 2.1.7 on 2019-10-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0028_auto_20191028_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addbooks',
            name='books_price',
            field=models.PositiveIntegerField(),
        ),
    ]
