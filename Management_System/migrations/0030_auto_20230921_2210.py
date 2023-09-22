# Generated by Django 2.2 on 2023-09-21 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0029_auto_20230921_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Department'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='dosage',
            field=models.PositiveIntegerField(),
        ),
    ]
