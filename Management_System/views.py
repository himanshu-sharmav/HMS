from django.shortcuts import get_object_or_404
from .models import Custom_User,Doctor,Patient,appointmentt,Department,Prescription,Navpane,User_Profile,Medical_Historyyy
from django.db.models import Q
from django_renderpdf.views import helpers
# from renderpdf import render
# from weasyprint import HTML 
from django.core.mail import send_mail
# from reportlab.pdfgen import canvas
import datetime
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from django.http import JsonResponse,HttpResponse
import json
# from reportlab.pdfgen import canvas


def register(request):
    if request.method=='GET':
        department_choices = Department.objects.all().values_list('dep_name', flat=True)
        return JsonResponse({'dep_name': list(department_choices)}, safe=False)
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
        if not password:
           return JsonResponse({"message":"Fill the password"})
        if not email:
           return JsonResponse({"message":"Fill the email"})
        if not contact:
           return JsonResponse({"message":"Fill the contact"})
        if not first_name:
           return JsonResponse({"message":"Fill the first_name"})
        if not last_name:
           return JsonResponse({"message":"Fill the lastname"})
        if not address:
           return JsonResponse({"message":"Fill the address"})
        if not sex:
           return JsonResponse({"message":"Fill the sex"})
        if not date_of_birth:
           return JsonResponse({"message":"Fill the date of birth"})
        if not username:
           return JsonResponse({"message":"Fill the username"})
        if not user_type:
           return JsonResponse({"message":"Fill the user_type"})
       
           
        if user_type=='Doctor':  
            specialization=data['specialization']
            qualifications=data['qualification']
            availability=data['availability']
            experience=data['experience']
            fees=data['fees']
            department=data['department']

            departmentt = Department.objects.get(dep_name=department)
            if not departmentt:
               return JsonResponse({'message':'Department not exist'})

            if not specialization or not qualifications or not availability or not experience or not fees or not department:
               return JsonResponse({'message':'Fill all fields'})

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
             date_of_birth=date_of_birth,
             )
            # doctor_role = get_object_or_404(User_Profile, roles='Doctor')
            # user.roles.add(doctor_role)
            departmentt = Department.objects.get(dep_name=department)
            Doctor.objects.create(
            userd=user,
            specialization=specialization,
            qualifications=qualifications,
            availability=availability,
            experience=experience,
            fees=fees,
            doc=departmentt
            )  
            return JsonResponse({'Confirm':'Doctor Registered'},status=201)
        elif user_type=='Patient':
            height=data['height']
            weight=data['weight']
            blood_group=data['blood_group']
            
            if not height or not weight or not blood_group:
               return JsonResponse({'message':'Fill all fields for patients'},status=400)
            
            if Custom_User.objects.filter(email=email).exists():
               return JsonResponse({'message': 'A user with this email already exists'}, status=400)

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
             
             )
            patient_role = get_object_or_404(User_Profile, roles='Patient')
            user.roles.add(patient_role)
            Patient.objects.create(
                userd=user,
                height=height,
                weight=weight,
                blood_group=blood_group
            )
            return JsonResponse({'Confirm':'Patient Registered'},status=201)
        else:
            return JsonResponse({'message':'Please send user type'},status=400)
    

    else:
        return JsonResponse({'message':'wrong method'},status=405)
    
def login_view(request):
     if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        if not username or not password:
          return JsonResponse({'message':'Fill all the fields'})
        user = authenticate(request, username=username, password=password)
      
        if user is not None:
            if user.is_active:
                login(request, user)
              
                roles=[role.roles for role in user.roles.all()] 
               
                return JsonResponse({'message': roles})
               
            else:
                return JsonResponse({'message': 'User is not active'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
     else:
        return JsonResponse({'message': 'Wrong method'}, status=405)
     
def logout_view(request):
    logout(request)
    return JsonResponse({'message':'user logged out'})     
def book_appointment(request):
  user=request.user
  if request.method=='POST':  
   
    doctor_id = request.POST.get('doctor_id')
    date=request.POST.get('appointment_date')
    medical_files=request.FILES.get('medical_files')
    symptoms=request.POST.get('symptoms')
   
    if not doctor_id :
       return JsonResponse({'message':'Fill the doctor id'},status=400)
    if not date:
       return JsonResponse({'message':'Fill the appointment date'},status=400)
       
    appointment_dates =  datetime.datetime.strptime(date,"%Y-%m-%d").date()
      
    doctor=Doctor.objects.get(pk=doctor_id)
    if not doctor:
      return JsonResponse({'message': 'Doctor not found'}, status=404)
    patient = Patient.objects.get(userd=user)
    if not patient:
      return JsonResponse({'message': 'Patient not found'}, status=404)
    make_appointment=appointmentt(
       patients=patient,
       Doctor=doctor,
       appointment_date=appointment_dates,
       medical_files=medical_files,
       symptoms=symptoms
       ) 
    make_appointment.save()
    patients_payment=Patient.objects.get(userd=user)
    patients_payment.payment_history=True
    patients_payment.save()
    return JsonResponse({'message':'appointment booked successfully'})


  else:
        return JsonResponse({'message': 'Wrong method'}, status=405)  
def approve_appointment(request):
    user=request.user
    if request.method=='POST':
       data=json.loads(request.body)
       appointmentid=data['appointment_id']
       
       if not appointmentid:
         return JsonResponse({'message':'Fill all fields'},status=400)
       appoints=appointmentt.objects.get(id=appointmentid) 
      
       if not appoints:
            return JsonResponse({'message': 'Appointment not found'}, status=404)
      
       doctor=Doctor.objects.filter(userd=user).first()

       if user.roles.filter(roles='Receptionist').exists():

         if not appoints.approval_receiptionist:
           appoints.approval_receiptionist=True
           appoints.save()
           return JsonResponse({'Confirmation':'Approved BY Receiptionist'})
         
         return JsonResponse({'Confirmation':'Already Approved by Receiptionist'})
       elif doctor and user== appoints.Doctor.userd:
        if appoints.approval_receiptionist: 
         if  appoints.approval_doctor==False: 
          appoints.approval_doctor=True
          appoints.save()

          if appoints.approval_receiptionist==True and appoints.approval_doctor==True:
             appoints.approval=True
             appoints.save()
             template_name = 'email_template/email_generate.html'
             context={
                'patient': appoints.patients,
                'doctor': appoints.Doctor,
                'appoint': appoints
             } 
             message=render_to_string(template_name,context) 
             patient_email=[appoints.patients.userd.email]
             print(patient_email)
             send_mail('Appointment Confirmation','','himan9506492198@gmail.com',patient_email,html_message=message,fail_silently=False)
          return JsonResponse({'Confirmation':'Approved BY Doctor'})
         
         return JsonResponse({'Confirmation':'Already Confirmed by Doctor'})
        
        return JsonResponse({'Confirmation':'Not Approved By Receptionist'})
        
       return JsonResponse({'message':'Not authorized to approve'},status=403)
    
    return JsonResponse({'message': 'Wrong method'}, status=405) 

def reject_appointment(request):
    user=request.user
    if request.method=='POST':
      
      if user.roles.filter(roles='Receptionist').exists() or user.roles.filter(roles='Doctor').exists():

        data=json.loads(request.body)
        appointmentid=data['appointment_id']
        reason=data['reason']
        if not appointmentid or not reason:
         return JsonResponse({'message':'Fill all fields'},status=400)
        
        appoint=appointmentt.objects.get(pk=appointmentid)
        if not appoint:
                return JsonResponse({'message': 'Appointment not found'}, status=404)
        if appoint.is_rejected==False:   
         appoint.is_rejected=True
         appoint.approval_receiptionist=True
         appoint.reasons=reason
         appoint.patients.payment_history=False
         appoint.save()
         
         template_name='email_template/reject_email.html'
         context={
            'patient':appoint.patients,
            'doctor':appoint.Doctor,
            'appoint':appoint
         }
         message=render_to_string(template_name,context) 
         patient_email=[appoint.patients.userd.email]
          
          
         send_mail('Appointment Rejection','','himan9506492198@gmail.com',patient_email,html_message=message,fail_silently=False)
 
         return JsonResponse({'message':'Appointment Rejected'})
        return JsonResponse({'message':'Appointment already Rejected. Kindly Refresh the Page.'}) 
      return JsonResponse({'message':'Not authorized to do this action'},status=403)  

    return JsonResponse({'message': 'Wrong method'}, status=405) 
    
def update_appointments(request):
   # user=request.user
   if request.method=='POST':
      data=json.loads(request.body)
      appointment_id=data['appointment_id']
      updated_date=data['updated_date']
      # medical_files=request.FILES.get('medical_files')
      
      if not appointment_id or not updated_date:
         return JsonResponse({'message':'Fill all fields'},status=400)  
      
      appointment_instance=appointmentt.objects.get(id=appointment_id)
      
      if not appointment_instance:
         return JsonResponse({'message': 'Appointment not found'}, status=404)

      if updated_date:
       appointment_instance.appointment_date=updated_date
       appointment_instance.save()
      # if medical_files:
      #    appointment_instance.medical_files=medical_files
      template_name='email_template/update_email.html'
      
      context={
           'patient':appointment_instance.patients,
           'doctor':appointment_instance.Doctor,
           'appoint':appointment_instance
        }
      
      message=render_to_string(template_name,context) 
      patient_email=[appointment_instance.patients.userd.email]

      send_mail('Appointment Update','','himan9506492198@gmail.com',patient_email,html_message=message,fail_silently=False)


      return JsonResponse({'message':'Appointment Date has been updated'})    
   
   return JsonResponse({'message': 'Method not allowed'}, status=405)  


def show_appointments(request):
   user=request.user
   if user.roles.filter(roles='Doctor').exists():
      appoints=appointmentt.objects.filter(Doctor__userd=user,is_rejected=False,approval_receiptionist=True,approval_doctor=False)
      
   elif user.roles.filter(roles='Receptionist').exists():
   
       appoints=appointmentt.objects.all()
   
   else:
       appoints = appointmentt.objects.filter(Q(patients__userd=user))

   appointment_list = [{'id': appointment.id,
                        'date': appointment.appointment_date.strftime('%Y-%m-%d'), 
                        'is_approved': appointment.approval,
                        'first_name':appointment.Doctor.userd.first_name,
                        'last_name':appointment.Doctor.userd.last_name,
                        'availability':appointment.Doctor.availability,
                        'department':appointment.Doctor.doc.dep_name,
                        'fees':appointment.Doctor.fees,
                        'Pfname':appointment.patients.userd.first_name,
                        'Plname':appointment.patients.userd.last_name,
                        'Rejection':appointment.is_rejected,
                        'Symptoms':appointment.symptoms,
                        'Receptionist':appointment.approval_receiptionist 
                        } 
                        for appointment in appoints
                        ]

   return JsonResponse({'message': appointment_list})

def medical_history(request):
  user=request.user
  if request.method=='GET':
    if user.is_authenticated:
     patient=Patient.objects.get(userd=user)
     med_history=Medical_Historyyy.objects.filter(userss=patient.id)
     if med_history:
        med_show=list(med_history.values())
       
        return JsonResponse({'med_details':med_show})
     else:
        return JsonResponse({'med_details':False})
    else:
         return JsonResponse({'message': 'Not authenticated'}, status=401)  

  if request.method=='POST':  
   if user.is_authenticated:
      data=json.loads(request.body)
      drugs=data['drugs']
      medication=data['medication']
      allergies=data['allergies']
      tobbaco_history=data['tobbaco_history']
      alcohol=data['alcohol']
      symptoms=data['symptoms']
      med_condition=data['med_condition']
      e_name=data['e_name']
      e_contact=data['e_contact']
   
      if not drugs or not medication or not allergies or not tobbaco_history or not alcohol or not symptoms or not med_condition or not e_name or not e_contact:
         return JsonResponse({'message':'Fill all fields'})
      
      patient=Patient.objects.get(userd=user)  
      Medical_Historyyy.objects.create( 
         userss=patient,
         drugs=drugs,
         medication=medication,
         allergies=allergies,
         tobbaco_history=tobbaco_history,
         alcohol=alcohol,
         symptoms=symptoms,
         med_condition=med_condition,
         emergency_name=e_name,
         emergency_contact=e_contact
      )  

      return JsonResponse({'message':'Medical History created'})
   else:
      return JsonResponse({'message':'not authenticated'},status=401)
   
  else:
      return JsonResponse({'message': 'Wrong method'}, status=405)   

def details_all(request):
 
 if request.method=='GET':
  user=request.user
  if user.is_authenticated: 
    if user.roles.filter(roles='Doctor').exists():
     
     appoints=appointmentt.objects.filter(Doctor__userd=user,approval_doctor=True)
     
     appointment_list = [{'id': appointment.id,
                          'date': appointment.appointment_date.strftime('%Y-%m-%d'), 
                          'is_approved': appointment.approval,
                          'first_name':appointment.Doctor.userd.first_name,
                          'last_name':appointment.Doctor.userd.last_name,
                          'availability':appointment.Doctor.availability,
                          'department':appointment.Doctor.doc.dep_name,
                          'fees':appointment.Doctor.fees,
                          'Pfname':appointment.patients.userd.first_name,
                          'Plname':appointment.patients.userd.last_name,
                          'Rejection':appointment.is_rejected,
                          'Symptoms':appointment.symptoms 
                          } 
                          for appointment in appoints
                          ]
            
     return JsonResponse({'message':appointment_list})
    
    else: 
         doctors=Doctor.objects.all().values('userd__first_name','userd__last_name','specialization','fees','availability','id','doc__dep_name')
         return JsonResponse(list(doctors),safe=False)
  
  else:
      return JsonResponse({'message': 'Not authenticated'}, status=401) 
 else:
        return JsonResponse({'message': 'Wrong method'}, status=405)


def get_details(request):
 if request.method=='GET':
 
  if request.user.is_authenticated:
   user = request.user
   if user.roles.filter(roles='Receptionist').exists():

      doctor_details = Doctor.objects.all().values('userd__first_name','userd__last_name','userd__sex','specialization','qualifications','experience','availability','doc__dep_name')
      patient_details=Patient.objects.all().values('userd__first_name','userd__last_name','blood_group','height','weight','userd__sex','userd__email','userd__contact')
      return JsonResponse({'doctor':list(doctor_details),'patients':list(patient_details)})
   
   elif user.roles.filter(roles='Patient').exists():

      patient=Patient.objects.get(userd=user)
      
 
      patient_data={
         'id': patient.id,
         "height":patient.height,
         "weight":patient.weight,
         "blood_group":patient.blood_group,
         
      }
      custom_user=patient.userd
      custom_user_data={
            'first_name': custom_user.first_name,
            'last_name': custom_user.last_name,
            'contact': custom_user.contact,
            'email': custom_user.email,
            'address': custom_user.address,
            'sex': custom_user.sex,
            'date_of_birth': custom_user.date_of_birth,
            'username': custom_user.username,
            # 'id': custom_user.id
      }
      combined_data={**patient_data,**custom_user_data}
   
      return JsonResponse({'patient':combined_data})
  
   elif user.roles.filter(roles='Doctor').exists():

      doctor_details=Doctor.objects.filter(userd=user).first()
      if doctor_details:
         excluded_details=['fees','availability','specialization']
         doctor_data=model_to_dict(doctor_details,exclude=excluded_details)
         custom_data = model_to_dict(doctor_details.userd, fields=['email', 'first_name', 'last_name', 'address', 'contact', 'sex', 'date_of_birth', 'username'])
         department_name=doctor_details.doc.dep_name
         combined_data = {**doctor_data, **custom_data,'department_name':department_name}
         return JsonResponse({'doctor':combined_data})
   else:
        return JsonResponse({'message':'user role not recognised'})
  else:
     return JsonResponse({'message':'user is not authenticated'})

 
def bill_view(request):
  
    if request.method == 'GET':
      
      appointment_id=request.GET.get('appointment_id')
      
      appointments=appointmentt.objects.get(id=appointment_id)
      
      patient=appointments.patients
      doctor=appointments.Doctor
      additional_costs=55
      total_amount=doctor.fees + additional_costs
      
      context={
      'patient': patient,
      'doctor':doctor,
      'additional_costs':additional_costs,
      'total_amount': total_amount
      }
      
      response = HttpResponse(content_type="application/pdf")
      response['Content-Disposition'] = f'attachment; filename="bill.pdf"'


      helpers.render_pdf(template=['billing_templates/bill_template.html'],file_=response,context=context)
      
      return response
    
    else:
        return JsonResponse({'message': 'Wrong method'}, status=405)
 
      
def department_details(request):
    if request.method =='GET':
       approved_count= appointmentt.objects.filter(approval=True).count()
       rejected_count=appointmentt.objects.filter(is_rejected=True).count()
       pending_count=appointmentt.objects.filter(approval=False,is_rejected=False).count()

       appointment_count= {
          'Approved':approved_count,
          'Rejected':rejected_count,
          'Pending':pending_count
       }

       return JsonResponse(appointment_count)
   #  if request.method == 'POST':
   #      data = json.loads(request.body)
   #      dep_name = data.get('dep_name')
   #      updated_name = data.get('new_name')
   #      dep_id = data.get('dep_id')

   #      if request.user.roles.filter(roles='Receptionist').exists():

   #          if dep_id and updated_name:
   #              dep_detail = Department.objects.filter(id=dep_id).first()
   #              if dep_detail:
   #                  dep_detail.dep_name = updated_name
   #                  dep_detail.save()
   #              else:
   #                  return JsonResponse({'message': 'Department not found'})

   #          else:
   #              Department.objects.create(dep_name=dep_name)
   #          return JsonResponse({'message': 'Department created'})
   #      else:
   #          return JsonResponse({"message": "No privilege"})

   #  elif request.method == 'DELETE':
   #    data = json.loads(request.body)
   #    dep_id = data.get('dep_id')
   #    if not dep_id:
   #          return JsonResponse({'message': 'Please provide department id'})
   #    if request.user.roles.filter(roles='Receptionist').exists():

   #      details = Department.objects.filter(id=dep_id).first()
   #      if details:
   #          details.is_status = True
   #          details.save()
   #          return JsonResponse({'message': 'Department Deleted'})
   #      else:
   #          return JsonResponse({'message': 'Department not found'})
def navpane(request):
   if request.method=='GET':
      user=request.user
      
      if user.roles.filter(roles='Patient').exists():

         rows=Navpane.objects.filter(worker_role='P').order_by('order')
      elif user.roles.filter(roles='Receptionist').exists():
         rows=Navpane.objects.filter(worker_role='R').order_by('order')
      else:
         rows=Navpane.objects.filter(worker_role='D').order_by('order')

      serialized_rows = [
            {
                'icon': row.icons,
                'state': row.state,
                'button_name': row.button_name,
            }
            for row in rows
        ]

      return JsonResponse(serialized_rows,safe=False)
   else:
      return JsonResponse({'message': 'Invalid request method'}, status=405)
         
      
def prescription(request):
   if request.method=='GET':
      user=request.user
      appointments_id=request.GET.get('appointment_id')
      if not appointments_id:
            return JsonResponse({'message': 'Please provide an appointment_id'}, status=400)
      
      appointments=appointmentt.objects.filter(id=appointments_id).first()
      if not appointments:
            return JsonResponse({'message': 'Appointment not found'}, status=404)
      user.roles.filter(roles='Doctor').exists()

      if user.roles.filter(roles='Doctor').exists():
      
         prescriptions = Prescription.objects.filter(patient_f=appointments, patient_f__Doctor__userd=user)
      else:
         prescriptions = Prescription.objects.filter(patient_f=appointments)

      all_prescriptions = []
      # reports_all= []
      # if user.roles.filter(roles='Doctor').exists():


      # else:
      #    appointments=appointmentt.objects.filter(patients__userd=user,id=appointments_id).first()

         # prescriptions = Prescription.objects.filter(patient_f=appointments)

      for prescription in prescriptions:
            prescription_data = {
                            'medicine': prescription.medicines,
                            'count': prescription.count,
                            'dosage': prescription.dosage,
                            'Report_name':prescription.Report_name,
                            'status':prescription.Status  
                        }
            all_prescriptions.append(prescription_data)
      # for reports in prescriptions:
      #    reports_data = {
      #                   'Report_name':reports.Report_name,
      #                   'status':reports.Status
      #    }
         # reports_all.append(reports_data)
      return JsonResponse({'medicines':all_prescriptions})
       

   elif request.method=='POST':
       data=json.loads(request.body)
       appointment_id=data.get('appointment_id')
       if not appointment_id:
            return JsonResponse({'message': 'Please provide an appointment_id'}, status=400)
       
       appointment_instance=appointmentt.objects.get(id=appointment_id)
       if not appointment_instance:
            return JsonResponse({'message': 'Appointment not found'}, status=404)
  
       prescription_data1 = data["data1"]
       prescription_data2 = data["data2"]
     
       for entry in prescription_data1:
          Report_name=entry.get('reportName')
          status=entry.get('reportStatus')
      
       for entry in prescription_data2:
          medical_name = entry.get('medicalName')
          medical_quantity = entry.get('medicalQuantity')
          dosage=entry.get('dosage')

          Prescription.objects.create(
           patient_f=appointment_instance,
           medicines=medical_name,
           count=medical_quantity,
           dosage=dosage,
           Report_name=Report_name,
           Status=status
           )
       return JsonResponse({'message':'Prescription Details Saved'})
   
   else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


def depart_count(request):
   if request.method=='GET':

      departments=Department.objects.all()

      department_info=[]

      for department in departments:
         doctor_count=Doctor.objects.filter(doc=department).count()
         department_info.append({'department_name':department.dep_name,'doctor_count':doctor_count})

      return JsonResponse(department_info,safe=False)   

   else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def all_users_count(request):

   # all_info = []
   
   doctor_count=Doctor.objects.all().count()
   patient_count=Patient.objects.all().count()

   # all_info.append({'doctor_count':doctor_count,'patient_count':patient_count})

   return JsonResponse({'doctor_count':doctor_count,'patient_count':patient_count})

def doctor_dashboard_chart(request):
   user=request.user   
   doctor_appointments=appointmentt.objects.filter(Doctor__userd=user)
   approved_appointments=doctor_appointments.filter(approval=True).count()
   reject_appointments=doctor_appointments.filter(is_rejected=True).count()

   male_patients_count = doctor_appointments.filter(patients__userd__sex='Male').count()
   female_patients_count = doctor_appointments.filter(patients__userd__sex='Female').count()
   return JsonResponse({
      'Approved_appointments':approved_appointments,
      'Rejected_appointments':reject_appointments,
      'Male_patients':male_patients_count,
      'Female_patients':female_patients_count
      })

def blood_group_chart(request):
   user=request.user
   doctor_appointments=appointmentt.objects.filter(Doctor__userd=user)
   blood_groups=['A-','A+','B+','B-','AB+','AB-','O+','O-']
   blood_group_counts = []

   for blood_group in blood_groups:
      count=doctor_appointments.filter(patients__blood_group=blood_group).count()
      blood_group_counts.append({
         'grp_name':blood_group,
         'patient_count':count
      })

   return JsonResponse(blood_group_counts,safe=False)   

   
def patient_chart(request):
   user= request.user

   patient_appointments=appointmentt.objects.filter(patients__userd=user)
   approved_count=patient_appointments.filter(approval=True).count()
   rejected_count=patient_appointments.filter(is_rejected=True).count()

   approval_counts = [
        {
            'approval_status': 'approved',
            'count': approved_count
        },
        {
            'approval_status': 'Rejected',
            'count': rejected_count
        }
    ]

   return JsonResponse(approval_counts,safe=False)

