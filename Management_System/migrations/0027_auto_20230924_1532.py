# Generated by Django 2.2 on 2023-09-24 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0026_auto_20230924_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medical_Histoy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alcohol', models.CharField(max_length=100, null=True)),
                ('symptoms', models.TextField(null=True)),
                ('tobbaco_history', models.CharField(max_length=100, null=True)),
                ('medication', models.CharField(max_length=100, null=True)),
                ('allergies', models.TextField(null=True)),
                ('med_condition', models.TextField(null=True)),
                ('drugs', models.CharField(max_length=100, null=True)),
                ('emergency_name', models.CharField(max_length=100, null=True)),
                ('emergency_contact', models.CharField(max_length=100, null=True)),
                ('userss', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Patient')),
            ],
        ),
        migrations.DeleteModel(
            name='Medical_Historyyy',
        ),
    ]
