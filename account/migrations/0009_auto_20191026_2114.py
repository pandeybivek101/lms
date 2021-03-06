# Generated by Django 2.1.7 on 2019-10-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20191024_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='barcode',
        ),
        migrations.AddField(
            model_name='user',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='std-barcode'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(upload_to='profile-pic'),
        ),
    ]
