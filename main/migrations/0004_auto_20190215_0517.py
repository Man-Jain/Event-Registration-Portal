# Generated by Django 2.1.7 on 2019-02-15 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190215_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
