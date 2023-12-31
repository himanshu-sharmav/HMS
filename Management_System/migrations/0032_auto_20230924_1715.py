# Generated by Django 2.2 on 2023-09-24 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0031_auto_20230924_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='appointmenttt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(null=True)),
                ('approval', models.BooleanField(default=False)),
                ('approval_receiptionist', models.BooleanField(default=False)),
                ('approval_doctor', models.BooleanField(default=False)),
                ('medical_files', models.FileField(null=True, upload_to='Document/')),
                ('reasons', models.TextField(null=True)),
                ('is_rejected', models.BooleanField(default=False, null=True)),
                ('Doctor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Doctor')),
            ],
        ),
        migrations.RemoveField(
            model_name='appointmentt',
            name='Doctor',
        ),
        migrations.RemoveField(
            model_name='appointmentt',
            name='patients',
        ),
        migrations.AlterField(
            model_name='patient',
            name='appointments',
            field=models.ManyToManyField(through='Management_System.appointmenttt', to='Management_System.Doctor'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient_prs',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.appointmenttt'),
        ),
        migrations.DeleteModel(
            name='appointment',
        ),
        migrations.DeleteModel(
            name='appointmentt',
        ),
        migrations.AddField(
            model_name='appointmenttt',
            name='patients',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Patient'),
        ),
    ]
