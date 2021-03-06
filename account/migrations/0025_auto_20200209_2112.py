# Generated by Django 2.1.7 on 2020-02-09 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_auto_20200209_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Faculty'),
        ),
        migrations.AddField(
            model_name='student',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flty', to='account.Faculty'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crs', to=settings.AUTH_USER_MODEL),
        ),
    ]
