from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'recent_diagnosis', 'diagnosis_date', 'treatment', 'allergens', 'past_diagnoses', 'past_treatments', 'notes']
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date'}),
            'allergens': forms.Textarea(attrs={'rows': 2}),
            'past_diagnoses': forms.Textarea(attrs={'rows': 3}),
            'past_treatments': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        
# from django import forms
# from .models import Patient

# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ['name', 'age', 'condition', 'diagnosis_date', 'treatment']
#         widgets = {
#             'diagnosis_date': forms.DateInput(attrs={'type': 'date'})
#         }