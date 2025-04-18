# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import PatientProfile, DoctorProfile, VerifierProfile

# User = get_user_model()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'patient':
#             PatientProfile.objects.create(user=instance)
#         elif instance.role == 'doctor':
#             DoctorProfile.objects.create(user=instance)
#         elif instance.role == 'verifier':
#             VerifierProfile.objects.create(user=instance)