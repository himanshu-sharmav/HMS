from django.shortcuts import get_object_or_404
from .models import Custom_User,Doctor,Patient,appointmentt,Department,Prescription,Navpane,User_Profile,Medical_Historyyy
from django.db.models import Q
# from Management_System import Custom_User
# from django_renderpdf.views import helpers
# from renderpdf import render
from weasyprint import HTML
from django.core.mail import send_mail

from django.template.loader import get_template
# from django.template import bill_template
from django.template import loader
# from reportlab.pdfgen import canvas
from django.shortcuts import render
# import reprlib
import datetime
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
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
        # if username or not password or not email or not contact or not first_name or not last_name or not address or not sex or not date_of_birth: 
        #    return JsonResponse({"message":"Fill All Fields"})
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
        # if not user_type:
        #    return JsonResponse({"message":"Fill the usertype"})
          
              
           
           
        if user_type=='Doctor':  
            specialization=data['specialization']
            qualifications=data['qualification']
            availability=data['availability']
            experience=data['experience']
            fees=data['fees']
            department=data['department']

            # sex=data['sex']
            # department_choices=Doctor.meta.get_field('department').choices
            # department=data['department']
            if not specialization or not qualifications or not availability or not experience or not fees:
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
            #  is_doctor=True
             )
            doctor_role = get_object_or_404(User_Profile, roles='Doctor')
            user.roles.add(doctor_role)
            
            # user_profile=  Custom_User.objects.create(user=user,is_doctor=True)
            Doctor.objects.create(
            userd=user,
            specialization=specialization,
            qualifications=qualifications,
            availability=availability,
            experience=experience,
            fees=fees,
            department=department
            )
            # user.roles.add(User_Profile.objects.get_or_create(name='Doctor')[0])   
            return JsonResponse({'Confirm':'Doctor Registered'})
        elif user_type=='Patient':
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
            #  is_doctor=False
             
             )
            # user_profile = User_Profile.objects.create(user=user)
            patient_role = get_object_or_404(User_Profile, roles='Patient')
            user.roles.add(patient_role)
            Patient.objects.create(
                userd=user,
                height=height,
                weight=weight,
                blood_group=blood_group
                
                # symptoms=symptoms
            )
            # user.roles.add(User_Profile.objects.get_or_create(name='Patient')[0])
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
        if not username or not password:
          return JsonResponse({'message':'Fill all the fields'})
        user = authenticate(request, username=username, password=password)
        # print(f"User authenticated: {user}")
        # print(f"User is_authenticated: {user.is_authenticated}")
        # user_a=Custom_User.objects.get(user.is_=True)
        if user is not None:
            if user.is_active:
                login(request, user)
               #  if user.is_superuser:
               #      return JsonResponse({'message':'R'})
                roles=[role.roles for role in user.roles.all()] 
               #  if  user.is_doctor==True:
                return JsonResponse({'message': roles})
               #  else:
               #      return JsonResponse({'message':'P'})
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
    # data=json.loads(request.body)
    doctor_id = request.POST.get('doctor_id')
    date=request.POST.get('appointment_date')
    medical_files=request.FILES.get('medical_files')
    symptoms=request.POST.get('symptoms')
    print(doctor_id)
    if not doctor_id :
       return JsonResponse({'message':'Fill id'},status=403)
    if not date:
       return JsonResponse({'message':'Fill date'})
       
    appointment_dates =  datetime.datetime.strptime(date,"%Y-%m-%d").date()

    doctor=Doctor.objects.get(pk=doctor_id)
    patient = Patient.objects.get(userd=user)
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
         return JsonResponse({'message':'Fill all fields'})
       appoints=appointmentt.objects.get(id=appointmentid) 
       doctor=Doctor.objects.filter(userd=user).first()
      #  send_mail(subject,confirmation_message,from_email,to_email,fail_silently=False,html_message=confirmation_message)  
       if user.roles.filter(roles='Receptionist').exists():

         if not appoints.approval_receiptionist:
           appoints.approval_receiptionist=True
           appoints.save()
           return JsonResponse({'Confirmation':'Approved BY Receiptionist'})
         else:
           return JsonResponse({'Confirmation':'Already Confirmed by Receiptionist'})
       elif doctor and user== appoints.Doctor.userd:
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
         else:
           return JsonResponse({'Confirmation':'Already Confirmed by Doctor'})
       else:
          return JsonResponse({'message':'Not authorized to approve'})

        # appoint.approval=True
        # appoint.save()
        # return JsonResponse({'message':'Appointment booked successful'})
      # else:
      #   return JsonResponse({'message': 'Not Receptionist or Doctor'}, status=400)
    else:
        return JsonResponse({'message': 'Wrong method'}, status=405) 

def reject_appointment(request):
    user=request.user
    if request.method=='POST':
      if user.is_superuser or user.is_doctor:
        data=json.loads(request.body)
        appointmentid=data['appointment_id']
        reason=data['reason']
        if not appointmentid:
         return JsonResponse({'message':'Fill all fields'})
        appoint=appointmentt.objects.get(pk=appointmentid)
        appoint.is_rejected=True
        appoint.reasons=reason
        appoint.save()
        template_name='email_template/reject_email.html'
        context={
           'patient':appoint.patients,
           'doctor':appoint.Doctor,
           'appoint':appoint
        }
        message=render_to_string(template_name,context) 
        patient_email=[appoint.patients.user.email]
         
         
        send_mail('Appointment Rejection','','himan9506492198@gmail.com',patient_email,html_message=message,fail_silently=False)

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
      # medical_files=request.FILES.get('medical_files')
      if not appointment_id or not updated_date:
         return JsonResponse({'message':'Fill all fields'},status=405)  
      appointment_instance=appointmentt.objects.get(id=appointment_id)
      if updated_date:
       appointment_instance.appointment_date=updated_date
       appointment_instance.save()
      # if medical_files:
      #    appointment_instance.medical_files=medical_files
      return JsonResponse({'message':'Appointment Date has been updated'})    

def show_appointments(request):
   user=request.user
   if user.roles.filter(roles='Doctor').exists():
      # doctor=Doctor.objects.get(user=user)
      appoints=appointmentt.objects.filter(Doctor__userd=user,is_rejected=False,approval_receiptionist=True,approval_doctor=False)
      
   elif user.roles.filter(roles='Receptionist').exists():
   
       appoints=appointmentt.objects.all()
      #  print(appoints) 
   else:
       appoints = appointmentt.objects.filter(Q(patients__userd=user))

   appointment_list = [{'id': appointment.id,'date': appointment.appointment_date.strftime('%Y-%m-%d'), 'is_approved': appointment.approval,'first_name':appointment.Doctor.userd.first_name,'last_name':appointment.Doctor.userd.last_name,'availability':appointment.Doctor.availability,'department':appointment.Doctor.doc.dep_name,'fees':appointment.Doctor.fees,'Pfname':appointment.patients.userd.first_name,'Plname':appointment.patients.userd.last_name,'Rejection':appointment.is_rejected } for appointment in appoints]


   return JsonResponse({'message': appointment_list})

def medical_history(request):
  user=request.user
  if request.method=='GET':
     patient=Patient.objects.get(userd=user)
     med_history=Medical_Historyyy.objects.filter(userss=patient.id)
     if med_history:
        med_show=list(med_history.values())
        print(type(med_show))
        return JsonResponse({'med_details':med_show})
     else:
        return JsonResponse({'med_details':False})   
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
    #   patient_id=data['patient_id']
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
      return JsonResponse({'message':'wrong method'},status=405)
   
# def payment_history:

def details_all(request):
 if request.method=='GET':
  user=request.user
  if user.roles.filter(roles='Doctor').exists():
   # user_id=user.id
   appoints=appointmentt.objects.filter(Doctor__userd=user,approval_doctor=True)
   # docs_data = [model_to_dict(appointment) for appointment in docs_]
   appointment_list = [{'id': appointment.id,'date': appointment.appointment_date.strftime('%Y-%m-%d'), 'is_approved': appointment.approval,'first_name':appointment.Doctor.userd.first_name,'last_name':appointment.Doctor.userd.last_name,'availability':appointment.Doctor.availability,'department':appointment.Doctor.doc.dep_name,'fees':appointment.Doctor.fees,'Pfname':appointment.patients.userd.first_name,'Plname':appointment.patients.userd.last_name,'Rejection':appointment.is_rejected,'Symptoms':appointment.symptoms } for appointment in appoints]
          
   return JsonResponse({'message':appointment_list})
  else: 
   doctors=Doctor.objects.all().values('userd__first_name','userd__last_name','specialization','fees','availability','id','doc__dep_name')
   return JsonResponse(list(doctors),safe=False)

def get_details(request):
 if request.method=='GET':
  if request.user.is_authenticated:
   user = request.user
   if user.roles.filter(roles='Receptionist').exists():

      doctor_details = Doctor.objects.all().values('userd__first_name','userd__last_name','userd__sex','specialization','qualifications','experience','availability','doc__dep_name')
      patient_details=Patient.objects.all().values('userd__first_name','userd__last_name','blood_group','height','weight','userd__sex','userd__email','userd__contact')
      return JsonResponse({'doctor':list(doctor_details),'patients':list(patient_details)})
   try:
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
    #   patient.pop('prescription', None)  
    #   patient.prescription = None
    #   patient_data = list(patient)
      return JsonResponse({'patient':combined_data})
  #  elif doctor:
   except Patient.DoesNotExist:
      doctor_details=Doctor.objects.filter(userd=user).first()
      if doctor_details:
         excluded_details=['fees','availability','specialization']
         doctor_data=model_to_dict(doctor_details,exclude=excluded_details)
         custom_data = model_to_dict(doctor_details.userd, fields=['email', 'first_name', 'last_name', 'address', 'contact', 'sex', 'date_of_birth', 'username'])
         combined_data = {**doctor_data, **custom_data}
         return JsonResponse({'doctor':combined_data})
      else:
        return JsonResponse({'message':'user role not recognised'})
  else:
     return JsonResponse({'message':'user is not authenticated'})

   
#  class bill_view(PDFView):   
#   template_name = 'billing_templates/bill_template.html'
 
def bill_view(request):
   # user=request.user
    if request.method == 'POST':
      # bill_Template='bill_template.html'

      template_name ='billing_templates/bill_template.html'
      # template_name = render_to_string('bill_template.html')

      # temp_n=get_template
      data=json.loads(request.body)
      appointment_id=data['appointment_id']
      # patient_id=data['patient_id']
      # doctor_id=data['doctor_id']
      appointments=appointmentt.objects.get(id=appointment_id)
      # patient=Patient.objects.filter(id=appointments.patients).first()
      # doctor=Doctor.objects.filter(id=appointments.Doctor).first()
      patient=appointments.patients
      doctor=appointments.Doctor
      additional_costs=55
      total_amount=doctor.fees + additional_costs
      # html_content = Template.render(context)
      context={
      'patient': patient,
      'doctor':doctor,
      'additional_costs':additional_costs,
      'total_amount': total_amount
      }
      # pdf_view=PDFView()
      # pdf= helpers.render_pdf(template=(template_name),file_='/home',context=context)
      # pdf = helpers.render_pdf(template=template_name,context=context,file_='/home')

      html_string = render_to_string(template_name, context, request=request)
      # html_string =  template_name.render(context)
      # pdf = HTML(string=html_string).write_pdf()
      # response = HttpResponse(pdf, content_type='application/pdf')
      # html = HTML(string=html_string)
      # pdf_file=pdf.write()
      # response['Content-Disposition'] = 'attachment; filename="bill.pdf"'
      # return response

      # pdf = render(request,template_name,context)
      # response= HttpResponse(pdf_file, content_type='application/pdf')
      # response['Content-Disposition'] = f'attachement; filename="bill.pdf"'
      # pdf_view=PDFView()
      
      response= HttpResponse(html_string, content_type='application/templates/pdf')
      response['Content-Disposition'] = f'attachement; filename="bill.pdf"'
      return response
      # return HttpResponse(template_name.render(context,request))
      # return JsonResponse({'message  ': 'POST request received'})
def department_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dep_name = data.get('dep_name')
        updated_name = data.get('new_name')
        dep_id = data.get('dep_id')

        if request.user.is_superuser:
            # if not dep_name:
            #     return JsonResponse({'message': 'Please provide department name'})

            if dep_id and updated_name:
                dep_detail = Department.objects.filter(id=dep_id).first()
                if dep_detail:
                    dep_detail.dep_name = updated_name
                    dep_detail.save()
                else:
                    return JsonResponse({'message': 'Department not found'})

            else:
                Department.objects.create(dep_name=dep_name)
            return JsonResponse({'message': 'Department created'})
        else:
            return JsonResponse({"message": "No privilege"})

    elif request.method == 'DELETE':
      data = json.loads(request.body)
      dep_id = data.get('dep_id')
      if not dep_id:
            return JsonResponse({'message': 'Please provide department id'})
      if request.user.is_superuser:
        details = Department.objects.filter(id=dep_id).first()
        if details:
            details.is_status = True
            details.save()
            return JsonResponse({'message': 'Department Deleted'})
        else:
            return JsonResponse({'message': 'Department not found'})
def navpane(request):
   if request.method=='GET':
      user=request.user
      
      if user.roles.filter(roles='Patient').exists():

         rows=Navpane.objects.filter(worker_role='P')
      elif user.roles.filter(roles='Receptionist').exists():
         rows=Navpane.objects.filter(worker_role='R')
      else:
         rows=Navpane.objects.filter(worker_role='D')

      serialized_rows = [
            {
                'icon': row.icons,
                'state': row.state,
                'button_name': row.button_name,
            }
            for row in rows
        ]
      # if len(serialized_rows)>=2:
      #    serialized_rows[0],serialized_rows[1]=serialized_rows[1],serialized_rows[0]

      return JsonResponse(serialized_rows,safe=False)
         
      
         # return JsonResponse({'components':'Patients,Appointments,Reports','icons':''})
      
def prescription(request):
   if request.method=='GET':
      user=request.user
      appointments_id=request.GET.get('appointment_id')
      appointments=appointmentt.objects.filter(patients__userd=user,id=appointments_id).first()
      # prescriptions = Prescription.objects.filter(patient_prs__patients__user=user)
      all_prescriptions = []
      reports_all= []

      # for appoint in appointments:
                  #   Retrieve prescriptions associated with the current appointment
      prescriptions = Prescription.objects.filter(patient_f=appointments)

      for prescription in prescriptions:
            prescription_data = {
                            'medicine': prescription.medicines,
                            'count': prescription.count,
                            'dosage': prescription.dosage,
                           #  'appointment_id': prescription.patient_f,
                            'Report_name':prescription.Report_name,
                            'status':prescription.Status
                        }
            all_prescriptions.append(prescription_data)
      for reports in prescriptions:
         reports_data = {
                        'Report_name':reports.Report_name,
                        'status':reports.Status
         }
         reports_all.append(reports_data)
      return JsonResponse({'medicines':all_prescriptions,'report':reports_all})
       
                
      

      # return JsonResponse({'Details': list(prescriptions)})



   if request.method=='POST':
       data=json.loads(request.body)
       appointment_id=data.get('appointment_id')
      # Report_name=
       appointment_instance=appointmentt.objects.get(id=appointment_id)
      # if "data" in data and isinstance(data["data"], list):
       prescription_data1 = data["data1"]
       prescription_data2 = data["data2"]
      #  print(prescription_data1)
      #  print(prescription_data2)

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