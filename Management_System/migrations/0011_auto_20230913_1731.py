# Generated by Django 2.2 on 2023-09-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0010_auto_20230913_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='payment_history',
            field=models.BooleanField(default=False),
        ),
    ]
