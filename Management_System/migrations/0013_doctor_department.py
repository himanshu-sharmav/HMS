# Generated by Django 2.2 on 2023-09-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0012_doctor_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='department',
            field=models.CharField(default='Cardiologist', max_length=50),
        ),
    ]
