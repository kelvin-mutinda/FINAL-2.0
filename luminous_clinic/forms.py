# luminous_clinic_project/luminous_clinic/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, PatientProfile, DoctorProfile, VerifierProfile, Service, Booking, Prescription, Payment, Notification, ChatMessage, PatientRecord

class CustomUserCreationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, initial='patient')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'role']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.username = user.email
        user.role = self.cleaned_data.get('role') or 'patient'
        if commit:
            user.save()
        return user

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['full_name', 'age', 'gender', 'phone_number', 'location', 'profile_picture']

class DoctorProfileForm(forms.ModelForm):
    selected_service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        label='Selected Service',
        required=True
    )

    class Meta:
        model = DoctorProfile
        fields = ['full_name', 'phone_number', 'gender', 'selected_service', 'verification_documents', 'profile_picture']

class VerifierProfileForm(forms.ModelForm):
    class Meta:
        model = VerifierProfile
        fields = ['full_name', 'phone_number', 'gender']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'duration', 'notes']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service']