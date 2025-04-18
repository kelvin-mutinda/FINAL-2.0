from django.apps import AppConfig

class LuminousClinicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'luminous_clinic'

    def ready(self):
        import luminous_clinic.signals