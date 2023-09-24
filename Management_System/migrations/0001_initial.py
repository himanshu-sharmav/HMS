# Generated by Django 2.2 on 2023-09-23 15:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='appointmentt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(null=True)),
                ('approval', models.BooleanField(default=False)),
                ('approval_receiptionist', models.BooleanField(default=False)),
                ('approval_doctor', models.BooleanField(default=False)),
                ('medical_files', models.FileField(null=True, upload_to='Document/')),
                ('reasons', models.TextField(null=True)),
                ('is_rejected', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=100, null=True)),
                ('is_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('availability', models.TextField()),
                ('experience', models.PositiveIntegerField()),
                ('fees', models.DecimalField(decimal_places=2, max_digits=8)),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Navpane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icons', models.TextField()),
                ('state', models.TextField()),
                ('button_name', models.TextField()),
                ('delete_sign', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Custom_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=300, null=True)),
                ('contact', models.CharField(max_length=20, null=True)),
                ('sex', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('roles', models.ManyToManyField(null=True, to='Management_System.User_Profile')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicines', models.CharField(max_length=200)),
                ('count', models.PositiveIntegerField(blank=True, null=True)),
                ('dosage', models.PositiveIntegerField()),
                ('patient_prs', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.appointmentt')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('weight', models.PositiveIntegerField(blank=True, null=True)),
                ('blood_group', models.CharField(max_length=5, null=True)),
                ('payment_history', models.BooleanField(default=False)),
                ('appointments', models.ManyToManyField(through='Management_System.appointmentt', to='Management_System.Doctors')),
                ('shared_navpane', models.ManyToManyField(blank=True, related_name='patients', to='Management_System.Navpane')),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medical_History',
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
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='doctors',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentt',
            name='Doctor',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Doctors'),
        ),
        migrations.AddField(
            model_name='appointmentt',
            name='patients',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Management_System.Patient'),
        ),
    ]
