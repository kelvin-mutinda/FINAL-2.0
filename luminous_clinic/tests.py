from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import PatientProfile, DoctorProfile, SymptomSubmission, Appointment, Prescription, Medication, Order, Payment

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_patient(self):
        user = User.objects.create_user(email='patient@example.com', password='testpass', role='patient')
        patient_profile = PatientProfile.objects.create(user=user, full_name='John Doe', phone_number='1234567890', gender='Male', date_of_birth='1990-01-01', address='123 Main St')
        self.assertEqual(str(patient_profile), 'John Doe')

    def test_create_doctor(self):
        user = User.objects.create_user(email='doctor@example.com', password='testpass', role='doctor')
        doctor_profile = DoctorProfile.objects.create(user=user, full_name='Jane Smith', phone_number='0987654321', gender='Female', medical_specialization='Cardiology')
        self.assertEqual(str(doctor_profile), 'Jane Smith')

class SymptomSubmissionModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='patient@example.com', password='testpass', role='patient')
        self.patient_profile = PatientProfile.objects.create(user=user, full_name='John Doe', phone_number='1234567890', gender='Male', date_of_birth='1990-01-01', address='123 Main St')

    def test_create_symptom_submission(self):
        symptom = SymptomSubmission.objects.create(patient=self.patient_profile, description='Headache')
        self.assertEqual(str(symptom), f"John Doe - {symptom.submitted_at}")

class AppointmentModelTest(TestCase):
    def setUp(self):
        patient_user = User.objects.create_user(email='patient@example.com', password='testpass', role='patient')
        self.patient_profile = PatientProfile.objects.create(user=patient_user, full_name='John Doe', phone_number='1234567890', gender='Male', date_of_birth='1990-01-01', address='123 Main St')
        
        doctor_user = User.objects.create_user(email='doctor@example.com', password='testpass', role='doctor')
        self.doctor_profile = DoctorProfile.objects.create(user=doctor_user, full_name='Jane Smith', phone_number='0987654321', gender='Female', medical_specialization='Cardiology')

    def test_create_appointment(self):
        appointment = Appointment.objects.create(patient=self.patient_profile, doctor=self.doctor_profile, scheduled_time='2023-10-01T10:00:00')
        self.assertEqual(str(appointment), f"John Doe - Jane Smith - {appointment.scheduled_time}")

class PrescriptionModelTest(TestCase):
    def setUp(self):
        patient_user = User.objects.create_user(email='patient@example.com', password='testpass', role='patient')
        self.patient_profile = PatientProfile.objects.create(user=patient_user, full_name='John Doe', phone_number='1234567890', gender='Male', date_of_birth='1990-01-01', address='123 Main St')
        
        doctor_user = User.objects.create_user(email='doctor@example.com', password='testpass', role='doctor')
        self.doctor_profile = DoctorProfile.objects.create(user=doctor_user, full_name='Jane Smith', phone_number='0987654321', gender='Female', medical_specialization='Cardiology')

    def test_create_prescription(self):
        prescription = Prescription.objects.create(patient=self.patient_profile, doctor=self.doctor_profile, medication='Paracetamol', dosage='1 tablet every 8 hours')
        self.assertEqual(str(prescription), f"John Doe - {prescription.issued_at}")

class MedicationModelTest(TestCase):
    def test_create_medication(self):
        medication = Medication.objects.create(name='Paracetamol', description='Pain reliever', price=5.00)
        self.assertEqual(str(medication), 'Paracetamol')

class OrderModelTest(TestCase):
    def setUp(self):
        patient_user = User.objects.create_user(email='patient@example.com', password='testpass', role='patient')
        self.patient_profile = PatientProfile.objects.create(user=patient_user, full_name='John Doe', phone_number='1234567890', gender='Male', date_of_birth='1990-01-01', address='123 Main St')
        
        self.medication = Medication.objects.create(name='Paracetamol', description='Pain reliever', price=5.00)

    def test_create_order(self):
        order = Order.objects.create(patient=self.patient_profile, medication=self.medication, quantity=2)
        self.assertEqual(str(order), f"John Doe - Paracetamol - 2")

class PaymentModelTest(TestCase):
    def setUp(self):
        patient_user = User.objects.create_user(email='patient@example.com', password='testpass', role='patient')
        self.patient_profile = PatientProfile.objects.create(user=patient_user, full_name='John Doe', phone_number='1234567890', gender='Male', date_of_birth='1990-01-01', address='123 Main St')
        
        doctor_user = User.objects.create_user(email='doctor@example.com', password='testpass', role='doctor')
        self.doctor_profile = DoctorProfile.objects.create(user=doctor_user, full_name='Jane Smith', phone_number='0987654321', gender='Female', medical_specialization='Cardiology')
        
        self.appointment = Appointment.objects.create(patient=self.patient_profile, doctor=self.doctor_profile, scheduled_time='2023-10-01T10:00:00')

    def test_create_payment(self):
        payment = Payment.objects.create(appointment=self.appointment, amount=10.00, transaction_id='TX123456789')
        self.assertEqual(str(payment), f"John Doe - 10.00")