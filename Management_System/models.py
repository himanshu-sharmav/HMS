from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import User


class User_Profile(models.Model):
    roles=models.TextField()
class Custom_User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=300,null=True)
    contact = models.CharField(max_length=20,null=True)
    sex=models.CharField(max_length=10,null=True)
    date_of_birth=models.DateField(null=True,blank=True)
    roles=models.ManyToManyField(User_Profile,null=True)


class Department(models.Model):
    dep_name=models.CharField(max_length=100,null=True)
    is_status=models.BooleanField(default=False)
# class Doctor(models.Model):
class Navpane(models.Model):
    icons=models.TextField()
    state=models.TextField()
    button_name=models.TextField()
    delete_sign=models.BooleanField(null=True)
    worker_role=models.CharField(max_length=50,null=True)
    order=models.PositiveIntegerField(default=0,null=True)
    class Meta:
        ordering= ['order']


class Doctor(models.Model):
    userd =models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
    specialization=models.CharField(max_length=100)
    qualifications = models.TextField()
    availability = models.TextField()
    experience = models.PositiveIntegerField()
    fees=models.DecimalField(max_digits=8,decimal_places=2)
    # department=models.CharField(max_length=50,default='Cardiologist')
    doc=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    # shared_navpane=models.ManyToManyField(Navpane,related_name='doctors',blank=True )
    

class Patient(models.Model):
    userd=models.ForeignKey(Custom_User,null=True,on_delete=models.CASCADE)
    height=models.PositiveIntegerField(blank=True,null=True)
    weight=models.PositiveIntegerField(blank=True,null=True)
    blood_group=models.CharField(max_length=5,null=True)
    payment_history = models.BooleanField(default=False)
    appointments=models.ManyToManyField(Doctor,through='appointmentt')
    shared_navpane=models.ManyToManyField(Navpane,related_name='patients',blank=True )
    # date_of_birth=models.DateField(null=True,blank=True)

class Medical_Historyyy(models.Model):
    # user=models.ForeignKey(Patient,on_delete=models.CASCADE,default=True)
    userss=models.ForeignKey(Patient,on_delete=models.CASCADE,default=True,null=True)
    
    # med_details=models.TextField(null=True)
    # medical_files=models.FileField(upload_to='Document/',null=True)
    alcohol=models.CharField(max_length=100,null=True)
    symptoms=models.TextField(null=True)
    tobbaco_history=models.CharField(max_length=100,null=True)
    medication=models.CharField(max_length=100,null=True)
    allergies=models.TextField(null=True)
    med_condition=models.TextField(null=True)
    drugs=models.CharField(max_length=100,null=True)
    emergency_name=models.CharField(max_length=100,null=True)
    emergency_contact=models.CharField(max_length=100,null=True)    
class appointmentt(models.Model):
    patients=models.ForeignKey(Patient,on_delete=models.CASCADE,default=True)
    Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,default=True)
    appointment_date=models.DateField(null=True)
    approval=models.BooleanField(default=False)
    approval_receiptionist=models.BooleanField(default=False)
    approval_doctor=models.BooleanField(default=False)
    medical_files=models.FileField(upload_to='Document/',null=True)
    reasons=models.TextField(null=True)
    is_rejected=models.BooleanField(null=True,default=False)  
    symptoms=models.CharField(max_length=100,null=True)


class Prescription(models.Model):
    # patient_prs=models.ForeignKey(appointmentt,on_delete=models.CASCADE,default=True)
    patient_f=models.ForeignKey(appointmentt,on_delete=models.CASCADE,default=True)


    medicines=models.CharField(max_length=200)
    count=models.PositiveIntegerField(blank=True,null=True)
    dosage=models.PositiveIntegerField()
    Report_name=models.CharField(max_length=100,null=True)
    Status=models.TextField(null=True)
    

    