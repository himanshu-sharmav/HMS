# Generated by Django 2.2 on 2023-09-24 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0015_auto_20230924_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medical_history',
            name='users',
        ),
        migrations.AddField(
            model_name='medical_history',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Patient'),
        ),
    ]
