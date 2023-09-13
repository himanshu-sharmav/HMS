# Generated by Django 2.2 on 2023-09-12 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0004_auto_20230912_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='department',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'), ('Allergists/Immunologists', 'Allergists/Immunologists'), ('Anesthesiologists', 'Anesthesiologists'), ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')], default='Cardiologist', max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='symptoms',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
