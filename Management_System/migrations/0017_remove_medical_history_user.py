# Generated by Django 2.2 on 2023-09-24 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0016_auto_20230924_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medical_history',
            name='user',
        ),
    ]
