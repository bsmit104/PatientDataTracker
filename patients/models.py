from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    recent_diagnosis = models.CharField(max_length=200, default="None")  # Was condition
    diagnosis_date = models.DateField()  # Most recent diagnosis date
    treatment = models.CharField(max_length=200, blank=True)  # Current treatment
    allergens = models.TextField(blank=True)  # Comma-separated list
    past_diagnoses = models.TextField(blank=True)  # Comma-separated list
    past_treatments = models.TextField(blank=True)  # Paired with past_diagnoses
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# from django.db import models
 
# class Patient(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     condition = models.CharField(max_length=200)
#     diagnosis_date = models.DateField()
#     treatment = models.CharField(max_length=200, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
