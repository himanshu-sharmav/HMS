from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import User

# from Management_System.views import department_details

# departments=[('Cardiologist','Cardiologist'),
# ('Dermatologists','Dermatologists'),
# ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
# ('Allergists/Immunologists','Allergists/Immunologists'),
# ('Anesthesiologists','Anesthesiologists'),
# ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
# ]
class User_Profile(models.Model):
    roles=models.TextField()
class Custom_User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=300,null=True)
    contact = models.CharField(max_length=20,null=True)
    sex=models.CharField(max_length=10,null=True)
    date_of_birth=models.DateField(null=True,blank=True)
    # is_doctor=models.BooleanField(default=False)
    # roles=models.ManyToManyField(User_Profile,null=True)
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
class Doctor(models.Model):
    userd =models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
    specialization=models.CharField(max_length=100)
    qualifications = models.TextField()
    availability = models.TextField()
    experience = models.PositiveIntegerField()
    fees=models.DecimalField(max_digits=8,decimal_places=2)
    department=models.CharField(max_length=50,default='Cardiologist')
    doc=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    # shared_navpane=models.ManyToManyField(Navpane,related_name='doctors',blank=True )

# class Doctors(models.Model):
#     user =models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
#     specialization=models.CharField(max_length=100)
#     qualifications = models.TextField()
#     availability = models.TextField()
#     experience = models.PositiveIntegerField()
#     fees=models.DecimalField(max_digits=8,decimal_places=2)
#     # department=models.CharField(max_length=50,choices=departments,default='Cardiologist')
#     doc=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
#     class Meta:
#         db_table="Doctor"
    # shared_navpane=models.ManyToManyField(Navpane,related_name='doctors',blank=True )    
    

class Patient(models.Model):
    userd=models.ForeignKey(Custom_User,null=True,on_delete=models.CASCADE)
    # your_id = models.AutoField(primary_key=True,default=0)
    # medical_history=models.FileField(upload_to='Patient/medical_history',null=True,blank=True)
    # medical_history=models.TextField(blank=True)``
    height=models.PositiveIntegerField(blank=True,null=True)
    weight=models.PositiveIntegerField(blank=True,null=True)
    blood_group=models.CharField(max_length=5,null=True)
    payment_history = models.BooleanField(default=False)
    # symptoms=models.CharField(max_length=100,null=True)
    # prescription=models.FileField(upload_to='Patient/prescription',null=True,blank=True)
    appointments=models.ManyToManyField(Doctor,through='appointmentt')
    shared_navpane=models.ManyToManyField(Navpane,related_name='patients',blank=True )
    # date_of_birth=models.DateField(null=True,blank=True)

# class Medical_History(models.Model):
#     user=models.ForeignKey(Patient,on_delete=models.CASCADE,default=True)
#     # user=models.ForeignKey(Patient,on_delete=models.CASCADE,default=True,null=True)
    
#     # med_details=models.TextField(null=True)
#     # medical_files=models.FileField(upload_to='Document/',null=True)
#     alcohol=models.CharField(max_length=100,null=True)
#     symptoms=models.TextField(null=True)
#     tobbaco_history=models.CharField(max_length=100,null=True)
#     medication=models.CharField(max_length=100,null=True)
#     allergies=models.TextField(null=True)
#     med_condition=models.TextField(null=True)
#     drugs=models.CharField(max_length=100,null=True)
#     emergency_name=models.CharField(max_length=100,null=True)
#     emergency_contact=models.CharField(max_length=100,null=True)
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
# class appointment(models.Model):
#     patients=models.ForeignKey(Patient,on_delete=models.CASCADE,default=True)
#     Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,default=True)
#     appointment_date=models.DateField(null=True)
#     approval=models.BooleanField(default=False)
#     approval_receiptionist=models.BooleanField(default=False)
#     approval_doctor=models.BooleanField(default=False)
#     medical_files=models.FileField(upload_to='Document/',null=True)
#     reasons=models.TextField(null=True)
#     is_rejected=models.BooleanField(null=True,default=False)
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

class Prescription(models.Model):
    patient_prs=models.ForeignKey(appointmentt,on_delete=models.CASCADE,default=True)
    medicines=models.CharField(max_length=200)
    count=models.PositiveIntegerField(blank=True,null=True)
    dosage=models.PositiveIntegerField()
    

    