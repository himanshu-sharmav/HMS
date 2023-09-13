from django.shortcuts import get_object_or_404
from .models import Custom_User,Doctor,Patient,appointment
# from Management_System import Custom_User
from django.contrib.auth import login,authenticate
from django.http import JsonResponse
from django.utils import timezone
import json


def register(request):
    if request.method=='GET':
        department_choices = dict(Doctor._meta.get_field('department').choices)
        # department_names = list(department_choices.keys())
        return JsonResponse({'department_names':department_choices})
    if request.method=='POST':
        data=json.loads(request.body)
        user_type=data['user_type']
        username=data['username']
        password=data['password']
        email=data['email']
        contact=data['contact']
        first_name=data['first_name']
        last_name=data['last_name']
        address=data['address']
        sex=data['sex']
        date_of_birth=data['date_of_birth']
        if user_type=='True':  
            specialization=data['specialization']
            qualifications=data['qualification']
            availability=data['availability']
            experience=data['experience']
            fees=data['fees']
            # sex=data['sex']
            # department_choices=Doctor.meta.get_field('department').choices
            department=data['department']
            



            if Custom_User.objects.filter(email=email).exists():
                return JsonResponse({'message':'Jhoola Chaap Doctor'})

            user=Custom_User.objects.create_user(
             username=username,
             email=email,
             contact=contact,
             first_name=first_name,
             last_name=last_name,
             sex=sex,
             password=password,
             address=address,
             date_of_birth=date_of_birth
             
             )
            
            # user_profile=  Custom_User.objects.create(user=user,is_doctor=True)
            Doctor.objects.create(
            user=user,
            specialization=specialization,
            qualifications=qualifications,
            availability=availability,
            experience=experience,
            fees=fees,
            department=department,
            is_doctor=True
            )

            return JsonResponse({'Confirm':'Doctor Registered'})
        elif user_type=='False':
            height=data['height']
            weight=data['weight']
            blood_group=data['blood_group']

            # symptoms=data['symptoms']
            # user_profile=  User_Profile.objects.create(user=user,is_doctor=False)
            user=Custom_User.objects.create_user(
             username=username,
             email=email,
             contact=contact,
             first_name=first_name,
             last_name=last_name,
             sex=sex,
             password=password,
             address=address,
             date_of_birth=date_of_birth,
             is_doctor=False
             
             )
            # user_profile = User_Profile.objects.create(user=user)
            Patient.objects.create(
                user=user,
                height=height,
                weight=weight,
                blood_group=blood_group
                
                # symptoms=symptoms
            )
            return JsonResponse({'Confirm':'Patient Registered'})
        else:
            return JsonResponse({'message':'Please send user type'})


    else:
        return JsonResponse({'message':'wrong method'},status=405)
    
def login_view(request):
     if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        print(f"User authenticated: {user}")
        # print(f"User is_authenticated: {user.is_authenticated}")
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return JsonResponse({'message':'R'})
                elif  Custom_User.is_doctor==True:
                  return JsonResponse({'message': 'D'})
                else:
                    return JsonResponse({'message':'P'})
            else:
                return JsonResponse({'message': 'User is not active'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
     else:
        return JsonResponse({'message': 'Wrong method'}, status=405)
     

def book_appointment(request):
  user=request.user
  if request.method=='POST':  
    data=json.loads(request.body)
    doctor_id=data['doctor__id']
    date=data['appointment_date']

    appointment_dates = timezone.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    doctor=Doctor.objects.get(pk=doctor_id)
    make_appointment=appointment(patients=user,Doctor=doctor,appointment_date=appointment_dates)
    make_appointment.save()
    return JsonResponse({'message':'appointment booked successfully'})


  else:
        return JsonResponse({'message': 'Wrong method'}, status=405)  
def approve_appointment(request):
    user=request.user
    if request.method=='POST':
      if user.is_superuser or user.is_doctor:
        data=json.loads(request.body)
        appointmentid=data['appointment_id']
        appoint=appointment.objects.get(pk=appointmentid)
        appoint.approval=True
        appoint.save()
        return JsonResponse({'message':'Appointment booked successful'})
      else:
        return JsonResponse({'message': 'Not Receptionist or Doctor'}, status=400)
    else:
        return JsonResponse({'message': 'Wrong method'}, status=405) 

def reject_appointment(request):

    user=request.user
    if request.method=='POST':
      if user.is_superuser or user.User_Profile.is_doctor:
        data=json.loads(request.body)
        appointmentid=data['appointment_id']
        appoint=appointment.objects.get(pk=appointmentid)
        appoint.approval=False
        appoint.save()
        return JsonResponse({'message':'Appointment Rejected'})

      else:
         return JsonResponse({'message':'Not authorized to do this action'},status=400)  

    else:
        return JsonResponse({'message': 'Wrong method'}, status=405) 
    
def update_appointments(request):
   user=request.user
   if request.method=='POST':
      data=json.loads(request.body)
      appointment_id=data['appointment_id']
      updated_date=data['updated_date']
      appointment_instance=appointment.objects.get(id=appointment_id)
      appointment_instance.appointment_date=updated_date
      appointment_instance.save()
      return JsonResponse({'message':'Appointment Date has been updated'})    
    
def show_appointments(request):
   user=request.user
   if user.Custom_user.is_doctor==True:
      appoints=appointment.objects.filter(Doctor=user)
      
   elif user.is_superuser:   
       appoints=appointment.objects.all()
   else:
       appoints=appointment.objects.filter(patients=user)

   appointment_list = [{'id': appointment.id, 'doctor': appointment.doctor.user.username, 'date': appointment.appointment_date.strftime('%Y-%m-%d %H:%M:%S'), 'is_approved': appointment.is_approved} for appointment in appoints]


   return JsonResponse({'message': appointment_list})

def Medical_History(request):
   user=request.user
   if user.is_authenticated:
      data=json.loads(request.body)
      drugs=data['drugs']
      medication=data['medication']
      allergies=data['allergies']
      tobbaco_history=data['tobbaco_history']
      alcohol=data['alcohol']
    #   patient_id=data['patient_id']
      patient=Patient.objects.get(user=user)  
      Medical_History.objects.create(
         patients=patient,
         drugs=drugs,
         medication=medication,
         allergies=allergies,
         tobbaco_history=tobbaco_history,
         alcohol=alcohol
      )  

      return JsonResponse({'message':'Medical History created'})
   else:
      return JsonResponse({'message':'wrong method'},status=405)
   
# def payment_history:

   
   
