# Generated by Django 2.2 on 2023-10-01 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0042_remove_doctor_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='roles',
            field=models.ManyToManyField(to='Management_System.User_Profile'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='fees',
            field=models.PositiveIntegerField(),
        ),
    ]