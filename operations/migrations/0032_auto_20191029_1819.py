# Generated by Django 2.1.7 on 2019-10-29 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0031_auto_20191029_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebooks',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='addbooks',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='std-barcode'),
        ),
    ]
