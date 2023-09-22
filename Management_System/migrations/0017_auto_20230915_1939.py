# Generated by Django 2.2 on 2023-09-15 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management_System', '0016_auto_20230915_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('approval', models.BooleanField(default=False)),
                ('Doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management_System.Doctor')),
                ('patients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management_System.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='appointments',
            field=models.ManyToManyField(through='Management_System.appointment', to='Management_System.Doctor'),
        ),
    ]
