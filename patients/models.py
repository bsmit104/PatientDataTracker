from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    # Existing fields...
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    recent_diagnosis = models.CharField(max_length=200, default="None")
    diagnosis_date = models.DateField()
    treatment = models.CharField(max_length=200, blank=True)
    allergens = models.TextField(blank=True)
    past_diagnoses = models.TextField(blank=True)
    past_treatments = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('added', 'Added'),
        ('edited', 'Edited'),
        ('deleted', 'Deleted'),
        ('viewed', 'Viewed'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    patient_name = models.CharField(max_length=100)  # Store name since patient might be deleted
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.patient_name} at {self.timestamp}"
 