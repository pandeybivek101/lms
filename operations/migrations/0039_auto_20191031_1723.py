# Generated by Django 2.1.7 on 2019-10-31 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0038_notice_opened'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notice',
            name='Postedon',
            field=models.DateField(auto_now_add=True),
        ),
    ]
