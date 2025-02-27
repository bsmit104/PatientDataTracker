from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from .models import Patient, ActionLog, EditHistory
from .forms import PatientForm
from collections import Counter
from datetime import datetime, timedelta
from django.http import HttpResponse
import csv

from patients import models

def patient_list(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(
            Q(name__icontains=query) |
            Q(recent_diagnosis__icontains=query) |
            Q(treatment__icontains=query) |
            Q(age__icontains=query) |
            Q(diagnosis_date__icontains=query)
        )
    else:
        patients = Patient.objects.all()
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed = Patient.objects.filter(id__in=recently_viewed_ids)[:5]
    recent_actions = ActionLog.objects.order_by('-timestamp')[:7]
    total_patients = Patient.objects.count()
    avg_age = Patient.objects.aggregate(avg_age=Avg('age'))['avg_age'] or 0
    top_diagnosis = Patient.objects.values('recent_diagnosis').annotate(count=Count('id')).order_by('-count').first()
    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'query': query,
        'recently_viewed': recently_viewed,
        'recent_actions': recent_actions,
        'total_patients': total_patients,
        'avg_age': round(avg_age, 1),
        'top_diagnosis': top_diagnosis['recent_diagnosis'] if top_diagnosis else 'N/A'
    })


def patient_chart(request):
    patients = Patient.objects.all()

    # Bar Chart: Patients per Age Group
    age_groups = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81+': 0}
    for p in patients:
        if p.age <= 20:
            age_groups['0-20'] += 1
        elif p.age <= 40:
            age_groups['21-40'] += 1
        elif p.age <= 60:
            age_groups['41-60'] += 1
        elif p.age <= 80:
            age_groups['61-80'] += 1
        else:
            age_groups['81+'] += 1
    bar_data = {
        'labels': list(age_groups.keys()),
        'counts': list(age_groups.values())
    }

    # Pie Chart: Most Common Recent Diagnoses
    diagnoses = [p.recent_diagnosis for p in patients if p.recent_diagnosis != "None"]
    diagnosis_counts = Counter(diagnoses).most_common(5)
    other_count = len(diagnoses) - sum(count for _, count in diagnosis_counts)
    pie_labels = [diag for diag, _ in diagnosis_counts] + (['Other'] if other_count > 0 else [])
    pie_values = [count for _, count in diagnosis_counts] + ([other_count] if other_count > 0 else [])
    pie_data = {
        'labels': pie_labels,
        'counts': pie_values
    }

    # Line Chart: Registrations Over Time (last 12 months)
    today = datetime.now().date()
    last_year = today - timedelta(days=365)
    monthly_counts = []
    labels = []
    current_date = last_year
    while current_date <= today:
        next_month = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        count = Patient.objects.filter(created_at__date__gte=current_date, created_at__date__lt=next_month).count()
        monthly_counts.append(count)
        labels.append(current_date.strftime('%b %Y'))
        current_date = next_month
    line_data = {
        'labels': labels,
        'counts': monthly_counts
    }

    # Heatmap: Diagnoses by Age Group
    heatmap_data = []
    diag_list = list(set(diagnoses))
    for diag in diag_list[:5]:  # Limit to top 5 for simplicity
        row = {'diagnosis': diag}
        for group in age_groups.keys():
            if group == '0-20':
                count = Patient.objects.filter(recent_diagnosis=diag, age__gte=0, age__lte=20).count()
            elif group == '21-40':
                count = Patient.objects.filter(recent_diagnosis=diag, age__gte=21, age__lte=40).count()
            elif group == '41-60':
                count = Patient.objects.filter(recent_diagnosis=diag, age__gte=41, age__lte=60).count()
            elif group == '61-80':
                count = Patient.objects.filter(recent_diagnosis=diag, age__gte=61, age__lte=80).count()
            elif group == '81+':
                count = Patient.objects.filter(recent_diagnosis=diag, age__gte=81).count()
            row[group] = count
        heatmap_data.append(row)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        chart_type = request.GET.get('type', 'bar')
        if chart_type == 'bar':
            return JsonResponse(bar_data)
        elif chart_type == 'pie':
            return JsonResponse(pie_data)
        elif chart_type == 'line':
            return JsonResponse(line_data)
        elif chart_type == 'heatmap':
            return JsonResponse({'data': heatmap_data})
    return render(request, 'patients/patient_chart.html')

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            ActionLog.objects.create(user=request.user, action='added', patient_name=patient.name)
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
            ActionLog.objects.create(user=request.user, action='edited', patient_name=patient.name)
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/edit_patient.html', {'form': form, 'patient': patient})

@login_required
def delete_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        ActionLog.objects.create(user=request.user, action='deleted', patient_name=patient.name)
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/delete_patient.html', {'patient': patient})


@login_required
def patient_detail(request, pk):
    patient = Patient.objects.get(pk=pk)
    recently_viewed = request.session.get('recently_viewed', [])
    if pk not in recently_viewed:
        recently_viewed.insert(0, pk)
        request.session['recently_viewed'] = recently_viewed[:5]
    ActionLog.objects.create(user=request.user, action='viewed', patient_name=patient.name)
    past_diagnoses = patient.past_diagnoses.split(',') if patient.past_diagnoses else []
    past_treatments = patient.past_treatments.split(',') if patient.past_treatments else []
    past_records = list(zip(past_diagnoses, past_treatments)) if past_diagnoses else []
    edit_history = patient.edit_history.all().order_by('-timestamp')[:5]  # Last 5 edits
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'past_records': past_records,
        'edit_history': edit_history
    })


@login_required
def edit_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            old_data = Patient.objects.get(pk=pk).__dict__
            form.save()
            new_data = Patient.objects.get(pk=pk).__dict__
            for field in form.changed_data:
                ActionLog.objects.create(user=request.user, action='edited', patient_name=patient.name)
                EditHistory.objects.create(
                    patient=patient,
                    user=request.user,
                    field_changed=field,
                    old_value=str(old_data.get(field, '')),
                    new_value=str(new_data.get(field, ''))
                )
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/edit_patient.html', {'form': form, 'patient': patient})



@login_required
def export_patients(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Recent Diagnosis', 'Diagnosis Date', 'Treatment', 'Allergens', 'Past Diagnoses', 'Past Treatments', 'Notes', 'Created At'])
    for patient in Patient.objects.all():
        writer.writerow([
            patient.name,
            patient.age,
            patient.recent_diagnosis,
            patient.diagnosis_date,
            patient.treatment,
            patient.allergens,
            patient.past_diagnoses,
            patient.past_treatments,
            patient.notes,
            patient.created_at
        ])
    ActionLog.objects.create(user=request.user, action='exported', patient_name='All Patients')
    return response