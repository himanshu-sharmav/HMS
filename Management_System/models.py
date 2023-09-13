from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import User

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Custom_User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=300,null=True)
    contact = models.CharField(max_length=20,null=True)
    sex=models.CharField(max_length=10,null=True)
    date_of_birth=models.DateField(null=True,blank=True)
    is_doctor=models.BooleanField(default=False)

# class Doctor(models.Model):
class Doctor(models.Model):
    user =models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
    specialization=models.CharField(max_length=100)
    qualifications = models.TextField()
    availability = models.TextField()
    experience = models.PositiveIntegerField()
    fees=models.DecimalField(max_digits=8,decimal_places=2)
    department=models.CharField(max_length=50,choices=departments,default='Cardiologist')
    

class Patient(models.Model):
    user=models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    # medical_history=models.FileField(upload_to='Patient/medical_history',null=True,blank=True)
    # medical_history=models.TextField(blank=True)``
    height=models.PositiveIntegerField(blank=True,null=True)
    weight=models.PositiveIntegerField(blank=True,null=True)
    blood_group=models.CharField(max_length=5,null=True)
    payment_history=models.TextField(blank=True)
    # symptoms=models.CharField(max_length=100,null=True)
    prescription=models.FileField(upload_to='Patient/prescription',null=True,blank=True)
    appointments=models.ManyToManyField(Doctor,through='appointment')
    # date_of_birth=models.DateField(null=True,blank=True)

class Medical_History(models.Model):
    user=models.ForeignKey(Patient,on_delete=models.CASCADE)
    drugs=models.CharField(max_length=5)
    allergies=models.CharField(max_length=50)
    medication=models.CharField(max_length=5)
    tobbaco_history=models.CharField(max_length=5)
    alcohol=models.CharField(max_length=20)
class appointment(models.Model):
    patients=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    appointment_date=models.DateTimeField()
    approval=models.BooleanField(default=False)

# class User_Profile(models.Model):
#     user=models.OneToOneField(Custom_User,on_delete=models.CASCADE)

