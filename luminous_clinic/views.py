# luminous_clinic_project/luminous_clinic/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PatientProfileForm, DoctorProfileForm, VerifierProfileForm, BookingForm, PrescriptionForm
from .models import CustomUser, PatientProfile, DoctorProfile, VerifierProfile, Booking, ChatMessage, Prescription, Payment, Notification, Service

def landing_page(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            if user.role == 'patient':
                return redirect('complete_patient_profile')
            elif user.role == 'doctor':
                return redirect('doctor_profile_setup')
            elif user.role == 'verifier':
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request, username=email, password=password, role=role)
        if user is not None:
            login(request, user)
            if user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'doctor':
                if user.doctor_profile.approved:
                    return redirect('doctor_dashboard')
                else:
                    return redirect('doctor_pending_approval')
            elif user.role == 'verifier':
                return redirect('verifier_dashboard')
        else:
            return render(request, 'login.html', {'form': CustomUserCreationForm(), 'error': 'Invalid credentials. Please check your email and password or create an account.'})
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('complete_patient_profile')
    
    # Check if patient profile is complete
    if not patient_profile.full_name or not patient_profile.age or not patient_profile.gender or not patient_profile.phone_number or not patient_profile.location:
        return redirect('complete_patient_profile')
    
    bookings = Booking.objects.filter(patient=patient_profile).order_by('-timestamp')
    pending_bookings = bookings.filter(status='Pending')
    accepted_bookings = bookings.filter(status='Accepted')
    
    return render(request, 'patient_dashboard.html', {
        'pending_bookings': pending_bookings,
        'accepted_bookings': accepted_bookings,
        'pending_count': pending_bookings.count(),
        'accepted_count': accepted_bookings.count(),
    })

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    try:
        doctor_profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_profile_setup')
    
    if not doctor_profile.approved:
        return redirect('doctor_pending_approval')
    
    bookings = Booking.objects.filter(
        service=doctor_profile.selected_service,
        status='Pending'
    ).order_by('timestamp')
    pending_count = bookings.count()
    accepted_count = Booking.objects.filter(
        service=doctor_profile.selected_service,
        status='Accepted'
    ).count()
    completed_count = Booking.objects.filter(
        service=doctor_profile.selected_service,
        status='Completed'
    ).count()
    
    return render(request, 'doctor_dashboard.html', {
        'bookings': bookings,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'completed_count': completed_count,
    })

@login_required
def verifier_dashboard(request):
    if request.user.role != 'verifier':
        return redirect('landing_page')
    
    pending_doctors = DoctorProfile.objects.filter(approved=False)
    return render(request, 'verifier_dashboard.html', {'pending_doctors': pending_doctors})

@login_required
def select_service(request):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('complete_patient_profile')
    
    # Check if patient profile is complete
    if not patient_profile.full_name or not patient_profile.age or not patient_profile.gender or not patient_profile.phone_number or not patient_profile.location:
        return redirect('complete_patient_profile')
    
    services = Service.objects.filter(is_active=True)
    if not services.exists():
        return render(request, 'select_service.html', {'services': [], 'error': 'No services available'})
    
    services_dict = {}
    for service in services:
        if service.category_name not in services_dict:
            services_dict[service.category_name] = []
        services_dict[service.category_name].append(service)
    
    return render(request, 'select_service.html', {'services_dict': services_dict})

@login_required
def book_service(request, service_id):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('complete_patient_profile')
    
    # Check if patient profile is complete
    if not patient_profile.full_name or not patient_profile.age or not patient_profile.gender or not patient_profile.phone_number or not patient_profile.location:
        return redirect('complete_patient_profile')
    
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.patient = patient_profile
            booking.service = service
            booking.save()
            Notification.objects.create(
                recipient=booking.patient.user,
                message="Your booking is pending approval.",
                read_status=False
            )
            # Notify all doctors linked to the selected service
            doctors = DoctorProfile.objects.filter(selected_service=service, approved=True)
            for doctor in doctors:
                Notification.objects.create(
                    recipient=doctor.user,
                    message=f"You have a new booking request from {booking.patient.full_name} for {service.service_name}.",
                    read_status=False
                )
            return redirect('patient_dashboard')
    else:
        form = BookingForm(initial={'service': service})
    return render(request, 'book_service.html', {'form': form})

@login_required
def accept_booking(request, booking_id):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    try:
        doctor_profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_profile_setup')
    
    if not doctor_profile.approved:
        return redirect('doctor_pending_approval')
    
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status == 'Pending':
        booking.status = 'Accepted'
        booking.doctor = doctor_profile
        booking.save()
        Notification.objects.create(
            recipient=booking.patient.user,
            message=f"Your request has been accepted by Dr. {doctor_profile.full_name}. Click chat to communicate with the doctor.",
            read_status=False
        )
        return redirect('chat', booking_id=booking.id)
    return redirect('doctor_dashboard')

@login_required
def reject_booking(request, booking_id):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    try:
        doctor_profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_profile_setup')
    
    if not doctor_profile.approved:
        return redirect('doctor_pending_approval')
    
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status == 'Pending':
        reason = request.POST.get('reason', 'No reason provided')
        booking.reason_for_rejection = reason
        booking.status = 'Rejected'
        booking.save()
        Notification.objects.create(
            recipient=booking.patient.user,
            message=f"Your request has been rejected by Dr. {doctor_profile.full_name}. Reason: {reason}",
            read_status=False
        )
    return redirect('doctor_dashboard')

@login_required
def chat(request, booking_id):
    if request.user.role not in ['patient', 'doctor']:
        return redirect('landing_page')
    
    booking = get_object_or_404(Booking, id=booking_id)
    messages = booking.messages.all().order_by('timestamp')
    
    if request.method == 'POST':
        message = request.POST['message']
        ChatMessage.objects.create(
            booking=booking,
            sender=request.user,
            receiver=booking.patient.user if request.user.role == 'doctor' else booking.doctor.user,
            message=message
        )
        return redirect('chat', booking_id=booking_id)
    
    return render(request, 'chat.html', {'booking': booking, 'messages': messages})

@login_required
def issue_prescription(request, booking_id):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    try:
        doctor_profile = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_profile_setup')
    
    if not doctor_profile.approved:
        return redirect('doctor_pending_approval')
    
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = booking.patient
            prescription.doctor = doctor_profile
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'create_prescription.html', {'form': form, 'booking': booking})

@login_required
def end_service(request, booking_id):
    if request.user.role not in ['patient', 'doctor']:
        return redirect('landing_page')
    
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user.role == 'doctor':
        if booking.status == 'Accepted':
            booking.status = 'Completed'
            booking.save()
            Notification.objects.create(
                recipient=booking.patient.user,
                message="The consultation has ended.",
                read_status=False
            )
            Notification.objects.create(
                recipient=booking.doctor.user,
                message="The consultation has ended.",
                read_status=False
            )
            return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        if booking.status == 'Accepted':
            booking.status = 'Completed'
            booking.save()
            Notification.objects.create(
                recipient=booking.patient.user,
                message="The consultation has ended.",
                read_status=False
            )
            Notification.objects.create(
                recipient=booking.doctor.user,
                message="The consultation has ended.",
                read_status=False
            )
            return redirect('patient_dashboard')
    
    return redirect('landing_page')

@login_required
def approve_doctor(request, doctor_id):
    if request.user.role != 'verifier':
        return redirect('landing_page')
    
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    if not doctor.approved:
        doctor.approved = True
        doctor.save()
        Notification.objects.create(
            recipient=doctor.user,
            message="Your profile has been approved. You can now start receiving patients.",
            read_status=False
        )
    return redirect('verifier_dashboard')

@login_required
def reject_doctor(request, doctor_id):
    if request.user.role != 'verifier':
        return redirect('landing_page')
    
    doctor_profile = get_object_or_404(DoctorProfile, pk=doctor_id)
    if not doctor_profile.approved:
        if request.method == 'POST':
            reason = request.POST.get('reason', '').strip()
            if reason:  # Ensure a reason is provided
                Notification.objects.create(
                    recipient=doctor_profile.user,
                    message=f"Your profile has been rejected. Reason: {reason}",
                    read_status=False
                )
                doctor_profile.delete()  # Delete the unapproved doctor profile
                return redirect('verifier_dashboard')
            else:
                return render(request, 'reject_doctor.html', {'doctor': doctor_profile, 'error': 'Reason is required.'})
        else:
            return render(request, 'reject_doctor.html', {'doctor': doctor_profile})
    return redirect('verifier_dashboard')

@login_required
def doctor_profile_setup(request):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    profile, created = DoctorProfile.objects.get_or_create(user=request.user)
    if profile.approved:
        return redirect('doctor_dashboard')
    
    services = Service.objects.filter(is_active=True)
    if not services.exists():
        return redirect('landing_page')  # Redirect to landing page if no services are available
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor_pending_approval')
    else:
        form = DoctorProfileForm(instance=profile)
    return render(request, 'doctor_profile_setup.html', {'form': form})

@login_required
def doctor_pending_approval(request):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    if hasattr(request.user, 'doctor_profile'):
        doctor_profile = request.user.doctor_profile
        if doctor_profile.approved:
            return redirect('doctor_dashboard')
    
    return render(request, 'doctor_pending_approval.html')

@login_required
def medical_records(request):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('complete_patient_profile')
    
    records = patient_profile.records.all().order_by('-timestamp')
    prescriptions = patient_profile.prescriptions.all().order_by('-issued_at')
    return render(request, 'medical_records.html', {
        'records': records,
        'prescriptions': prescriptions
    })

@login_required
def view_prescriptions(request):
    if request.user.role != 'doctor':
        return redirect('landing_page')
    
    prescriptions = Prescription.objects.all().order_by('-issued_at')
    return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

@login_required
def cancel_booking(request, booking_id):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('complete_patient_profile')
    
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status == 'Pending':
        booking.delete()
        Notification.objects.create(
            recipient=booking.patient.user,
            message=f"Booking by {patient_profile.full_name} has been canceled.",
            read_status=False
        )
    return redirect('patient_dashboard')

@login_required
def complete_patient_profile(request):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = PatientProfileForm(instance=profile)
    return render(request, 'complete_profile.html', {'form': form})

@login_required
def patient_profile(request):
    if request.user.role != 'patient':
        return redirect('landing_page')
    
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('complete_patient_profile')
    
    return render(request, 'patient_profile.html', {'profile': patient_profile})