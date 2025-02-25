from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm
from django.http import JsonResponse
from django.db.models import Q

# def patient_list(request):
#     patients = Patient.objects.all()
#     return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_list(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(
            Q(name__icontains=query) |
            Q(recent_diagnosis__icontains=query) |  # Changed from condition
            Q(treatment__icontains=query) |
            Q(age__icontains=query) |
            Q(diagnosis_date__icontains=query)
        )
    else:
        patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients, 'query': query})

# def patient_list(request):
#     query = request.GET.get('q', '')  # Get search query from URL
#     if query:
#         patients = Patient.objects.filter(
#             Q(name__icontains=query) |
#             Q(condition__icontains=query) |
#             Q(treatment__icontains=query) |
#             Q(age__icontains=query) |
#             Q(diagnosis_date__icontains=query)
#         )
#     else:
#         patients = Patient.objects.all()
#     return render(request, 'patients/patient_list.html', {'patients': patients, 'query': query})

def patient_chart(request):
    patients = Patient.objects.all()
    data = {
        'labels': [p.recent_diagnosis for p in patients],  # Changed from condition
        'ages': [p.age for p in patients]
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(data)
    return render(request, 'patients/patient_chart.html')


# def patient_chart(request):
#     patients = Patient.objects.all()
#     data = {
#         'labels': [p.condition for p in patients],
#         'ages': [p.age for p in patients]
#     }
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return JsonResponse(data)
#     return render(request, 'patients/patient_chart.html')

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/add_patient.html', {'form': form})

@login_required
def edit_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/edit_patient.html', {'form': form, 'patient': patient})

@login_required
def delete_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/delete_patient.html', {'patient': patient})



@login_required
def patient_detail(request, pk):
    patient = Patient.objects.get(pk=pk)
    # Split comma-separated fields into lists
    past_diagnoses = patient.past_diagnoses.split(',') if patient.past_diagnoses else []
    past_treatments = patient.past_treatments.split(',') if patient.past_treatments else []
    # Zip them together for template
    past_records = list(zip(past_diagnoses, past_treatments)) if past_diagnoses else []
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'past_records': past_records
    })


# import logging
# from django.shortcuts import render, redirect
# from .models import Patient
# import matplotlib.pyplot as plt
# import io
# import base64

# from .forms import PatientForm

# logger = logging.getLogger(__name__)

# def add_patient(request):
#     if request.method == 'POST':
#         form = PatientForm(request.POST)
#         if form.is_valid():
#             patient = form.save()
#             logger.info(f"Saved patient: {patient.name}, Treatment: {patient.treatment}")
#             return redirect('patient_list')
#     else:
#         form = PatientForm()
#     return render(request, 'patients/add_patient.html', {'form': form})

# def edit_patient(request, pk):
#     patient = Patient.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = PatientForm(request.POST, instance=patient)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_list')
#     else:
#         form = PatientForm(instance=patient)
#     return render(request, 'patients/edit_patient.html', {'form': form, 'patient': patient})

# def delete_patient(request, pk):
#     patient = Patient.objects.get(pk=pk)
#     if request.method == 'POST':
#         patient.delete()
#         return redirect('patient_list')
#     return render(request, 'patients/delete_patient.html', {'patient': patient})

# # def patient_list(request):
# #     patients = Patient.objects.all()
# #     return render(request, 'patients/patient_list.html', {'patients': patients})
# def patient_list(request):
#     patients = Patient.objects.all()
#     return render(request, 'patients/patient_list.html', {'patients': patients})

# from django.http import JsonResponse

# def patient_chart(request):
#     patients = Patient.objects.all()
#     data = {
#         'labels': [p.condition for p in patients],
#         'ages': [p.age for p in patients]
#     }
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return JsonResponse(data)
#     return render(request, 'patients/patient_chart.html')










# def patient_chart(request):
#     patients = Patient.objects.all()
#     ages = [p.age for p in patients]
#     conditions = [p.condition for p in patients]

#     plt.switch_backend('Agg')  # For non-interactive use
#     plt.bar(conditions, ages)
#     plt.xlabel('Condition')
#     plt.ylabel('Age')

#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()
#     graphic = base64.b64encode(image_png).decode('utf-8')
#     plt.close()

#     return render(request, 'patients/patient_chart.html', {'graphic': graphic})