# Generated by Django 2.2 on 2023-09-27 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0037_prescription_patient_f'),
    ]

    operations = [
        migrations.AddField(
            model_name='navpane',
            name='order',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]