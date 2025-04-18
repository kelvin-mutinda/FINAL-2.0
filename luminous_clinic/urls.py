from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Custom login URL
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),  # Custom logout URL
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('verifier-dashboard/', views.verifier_dashboard, name='verifier_dashboard'),
    path('select-service/', views.select_service, name='select_service'),
    path('book-service/<int:service_id>/', views.book_service, name='book_service'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('chat/<int:booking_id>/', views.chat, name='chat'),
    path('issue-prescription/<int:booking_id>/', views.issue_prescription, name='issue_prescription'),
    path('end-service/<int:booking_id>/', views.end_service, name='end_service'),
    path('approve-doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('reject-doctor/<int:doctor_id>/', views.reject_doctor, name='reject_doctor'),
    path('doctor-profile-setup/', views.doctor_profile_setup, name='doctor_profile_setup'),
    path('doctor-pending-approval/', views.doctor_pending_approval, name='doctor_pending_approval'),
    path('medical-records/', views.medical_records, name='medical_records'),
    path('view-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('complete-patient-profile/', views.complete_patient_profile, name='complete_patient_profile'),
    path('patient-profile/', views.patient_profile, name='patient_profile'),  # New URL pattern for patient profile
]