# Generated by Django 2.1.7 on 2019-10-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_student_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
