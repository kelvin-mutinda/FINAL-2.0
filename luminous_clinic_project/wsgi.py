import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luminous_clinic_project.settings')

application = get_wsgi_application()