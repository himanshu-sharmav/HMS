# Generated by Django 2.2 on 2023-09-28 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0039_auto_20230927_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='department',
        ),
    ]
