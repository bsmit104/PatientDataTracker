from django.shortcuts import render
from .models import Patient
import matplotlib.pyplot as plt
import io
import base64

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_chart(request):
    patients = Patient.objects.all()
    ages = [p.age for p in patients]
    conditions = [p.condition for p in patients]

    plt.switch_backend('Agg')  # For non-interactive use
    plt.bar(conditions, ages)
    plt.xlabel('Condition')
    plt.ylabel('Age')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return render(request, 'patients/patient_chart.html', {'graphic': graphic})