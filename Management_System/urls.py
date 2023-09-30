from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import bill_view

urlpatterns =[
    path('register',views.register,name='register'),
    path('login_view',views.login_view,name='login_view'),
    path('get_details',views.get_details,name='get_details'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('medical_history',views.medical_history,name='medical_history'),
    path('book_appointment',views.book_appointment,name='book_appointment'),
    path('bill_view',views.bill_view,name='bill_view'),
    path('details_all',views.details_all,name='details_all'),
    path('department_details',views.department_details,name='department_details'),
     path('show_appointments',views.show_appointments,name='show_appointments'),
     path('approve_appointment',views.approve_appointment,name='approve_appointment'),
     path('reject_appointment',views.reject_appointment,name='reject_appointment'),
     path('update_appointments',views.update_appointments,name='update_appointments'),
    path('prescription',views.prescription,name='prescription'),
    path('Elements',views.navpane,name='Elements'),
    path('depart_count',views.depart_count,name='depart_count'),
    path('users_count',views.all_users_count,name='users_count'),
    path('doctor_chart',views.doctor_dashboard_chart,name='doctor_chart'),
    path('blood_chart',views.blood_group_chart,name='blood_chart'),
    path('patient_chart',views.patient_chart,name='patient_chart'),





]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

