from django.core.management.base import BaseCommand
from patients.models import Patient
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Loads mock patient data'

    def handle(self, *args, **options):
        fake = Faker()
        conditions = ["Flu", "Diabetes", "Hypertension", "Asthma"]
        treatments = ["Rest", "Insulin", "Medication", "Inhaler", ""]
        allergens = ["Pollen", "Peanuts", "Dust", "None"]
        past_conditions = ["Cold", "Bronchitis", "Pneumonia", "Migraine"]
        past_treats = ["Antibiotics", "Painkillers", "Rest", "Inhaler"]
        for _ in range(60):
            past_diag_count = random.randint(0, 3)
            past_diags = ", ".join(random.sample(past_conditions, past_diag_count))
            past_treats_list = ", ".join(random.sample(past_treats, past_diag_count)) if past_diag_count else ""
            Patient.objects.create(
                name=fake.name(),
                age=random.randint(18, 90),
                recent_diagnosis=random.choice(conditions),
                diagnosis_date=fake.date_between(start_date="-1y", end_date="today"),
                treatment=random.choice(treatments),
                allergens=random.choice(allergens),
                past_diagnoses=past_diags,
                past_treatments=past_treats_list,
                notes=fake.text(max_nb_chars=200) if random.random() > 0.5 else ""
            )
        self.stdout.write(self.style.SUCCESS('Mock data loaded successfully'))
