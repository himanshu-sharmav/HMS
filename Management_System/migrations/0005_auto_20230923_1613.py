# Generated by Django 2.2 on 2023-09-23 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0004_auto_20230923_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='users',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
    ]
