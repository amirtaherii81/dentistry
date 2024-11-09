from django.shortcuts import render
from .models import Disease
from django.views import View
from apps.accounts.models import Patient
# from 
# Create your views here.

class BlogView(View):
    def get(self, request, *args, **kwargs):
        diseases = Disease.objects.filter(is_active=True).order_by('-is_priority')
        last_diseases = Disease.objects.filter(is_active=True).order_by('-publication_date')[:3]
        return render(request, 'diseases_app/blag.html', {'diseases': diseases, 'last_diseases':last_diseases})


def part_blog(request, id):
    patient = Patient.objects.get(pk=id)
    diseases_patient = patient.diseases.all()
    return render(request, 'diseases_app/part_blog.html', {'diseases_patient':diseases_patient})
    