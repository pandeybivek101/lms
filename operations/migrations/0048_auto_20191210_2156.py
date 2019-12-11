# Generated by Django 2.1.7 on 2019-12-10 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0047_issuebooks_returned_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebooks',
            name='book',
            field=models.FileField(help_text='Required. Please upload  an epub or pdf file.', upload_to='files', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('pdf', 'epub'))]),
        ),
    ]
