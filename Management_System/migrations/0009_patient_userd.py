# Generated by Django 2.2 on 2023-09-23 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0008_remove_patient_userd'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='userd',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
