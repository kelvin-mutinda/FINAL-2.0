# luminous_clinic_project/luminous_clinic/management/commands/populate_services.py

from django.core.management.base import BaseCommand
from luminous_clinic.models import Service

SERVICES_DATA = [
    {"service_code": "FAM001", "category_name": "General Consultation", "service_name": "Family Medicine", "description": "For common health concerns like colds, flu, fever, headaches, or general checkups. A family doctor gives advice or treatment."},
    {"service_code": "DEN001", "category_name": "Dentistry", "service_name": "Oral Health", "description": "For toothaches, bleeding gums, bad breath, or any dental issues. You may get advice, prescriptions, or be referred for a physical visit."},
    {"service_code": "PED001", "category_name": "Pediatrics", "service_name": "Pediatrics", "description": "Specialized care for babies, children, and teens — including cough, fever, nutrition, and growth monitoring."},
    {"service_code": "GYNO001", "category_name": "Gynecology & Obstetrics", "service_name": "Gynecology & Obstetrics", "description": "For women’s health issues, menstrual problems, pregnancy care, birth control advice, or menopause-related concerns."},
    {"service_code": "DERM001", "category_name": "Dermatology", "service_name": "Dermatology", "description": "Skin, hair, and nail care — including rashes, acne, eczema, hair loss, and skin infections."},
    {"service_code": "PSYCH001", "category_name": "Psychiatry", "service_name": "Mental Health Services", "description": "Get help with stress, anxiety, depression, insomnia, trauma, or emotional problems through licensed therapists or psychiatrists."},
    {"service_code": "NUTR001", "category_name": "Nutrition & Dietetics", "service_name": "Nutrition & Dietetics", "description": "Personalized diet plans, weight management, pregnancy nutrition, or help managing conditions like diabetes through food."},
    {"service_code": "IM001", "category_name": "Internal Medicine", "service_name": "Internal Medicine", "description": "For adult diseases like diabetes, high blood pressure, ulcers, infections, or chronic illness management."},
    {"service_code": "CARD001", "category_name": "Cardiology", "service_name": "Cardiology", "description": "Heart-related issues like chest pain, high blood pressure, palpitations, or heart disease follow-ups."},
    {"service_code": "ENDO001", "category_name": "Endocrinology", "service_name": "Endocrinology", "description": "Hormonal problems including thyroid disorders, diabetes, growth issues, or PCOS in women."},
    {"service_code": "ORTHO001", "category_name": "Orthopedics", "service_name": "Orthopedics", "description": "For joint pain, back pain, fractures, arthritis, and bone or muscle injuries."},
    {"service_code": "NEURO001", "category_name": "Neurology", "service_name": "Neurology", "description": "Brain and nerve-related issues like headaches, seizures, memory loss, or numbness."},
    {"service_code": "ENT001", "category_name": "ENT", "service_name": "Ear, Nose & Throat", "description": "For sore throat, ear pain, blocked nose, allergies, sinus issues, or hearing problems."},
    {"service_code": "URO001", "category_name": "Urology", "service_name": "Urology", "description": "For urinary issues, kidney problems, or male reproductive health like infections or prostate issues."},
    {"service_code": "GASTRO001", "category_name": "Gastroenterology", "service_name": "Gastroenterology", "description": "Stomach and digestive problems like ulcers, constipation, diarrhea, or liver issues."},
    {"service_code": "OPHTHA001", "category_name": "Ophthalmology", "service_name": "Eye Care", "description": "Eye infections, blurred vision, red eyes, or advice on eye conditions and prescriptions for glasses."},
    {"service_code": "ALLERGY001", "category_name": "Allergy & Immunology", "service_name": "Allergy & Immunology", "description": "Help with allergy testing, skin reactions, breathing problems, and immune system disorders."},
    {"service_code": "PULMO001", "category_name": "Pulmonology", "service_name": "Lung Care", "description": "For coughs, asthma, breathing difficulties, chest congestion, or COVID-19 follow-ups."},
    {"service_code": "SEXUAL001", "category_name": "Sexual Health & STD Consultation", "service_name": "Sexual Health & STD Consultation", "description": "Confidential help for sexually transmitted diseases (STDs), infections, sexual wellness, and safe practices."},
    {"service_code": "PHYSIO001", "category_name": "Physiotherapy & Rehabilitation", "service_name": "Physiotherapy & Rehabilitation", "description": "Virtual support for recovery after injury, surgery, or stroke — includes exercises and physical therapy advice."},
    {"service_code": "HOME001", "category_name": "Home Care Services", "service_name": "Home Care Services", "description": "Request a nurse or doctor to visit your home for care, especially useful for the elderly or bedridden patients."},
    {"service_code": "LAB001", "category_name": "Lab Test Booking & Results Review", "service_name": "Lab Test Booking & Results Review", "description": "Book tests online and get results reviewed by a doctor without visiting the hospital."},
    {"service_code": "VACCINE001", "category_name": "Vaccination Scheduling & Guidance", "service_name": "Vaccination Scheduling & Guidance", "description": "Help with planning your vaccinations (children or adults), reminders, and follow-up care."},
]

class Command(BaseCommand):
    help = 'Populates the Service table with predefined services'

    def handle(self, *args, **options):
        for service_data in SERVICES_DATA:
            service, created = Service.objects.get_or_create(
                service_code=service_data['service_code'],
                defaults={
                    'category_name': service_data['category_name'],
                    'service_name': service_data['service_name'],
                    'description': service_data['description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added service: {service.service_name} ({service.service_code})'))
            else:
                self.stdout.write(self.style.WARNING(f'Service already exists: {service.service_name} ({service.service_code})'))