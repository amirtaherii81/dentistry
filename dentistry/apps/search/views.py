from django.shortcuts import render, redirect
from django.views import View
from apps.diseases.models import Disease
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from apps.accounts.models import Patient
from django.http import Http404
# Create your views here.
         
# def search_patient(request):  
#     value = request.GET.get('value')
#     query = Disease.objects.get(Q(title__icontains=value) & Q(is_active=True))
#     response_data = {  
#         'diseaseName': query.title,  # نام بیماری  
#         'diseaseId': query.id  # شناسه بیماری  
#         }  
#     return JsonResponse(response_data)

def search_disease(request):  
    value = request.GET.get('value')  # ورودی کاربر  
    # جستجوی بیماری در لیست بیماری‌ها  
    diseases = Disease.objects.filter(Q(title__icontains=value) & Q(is_active=True))  
    
    # ساختار خروجی  
    response_data = []  
    for disease in diseases:  
        response_data.append({  
            'diseaseName': disease.title,  
            'diseaseId': disease.id  
        })  
    
    return JsonResponse(response_data, safe=False)


# def search_patient(request):
#     value = request.GET.get('value')
#     patient = Patient.objects.get(Q(is_active=True) & 
#                                 Q(name__icontains=value) | 
#                                 Q(family__icontains=value) | 
#                                 Q(phone_number__icontains=value) | 
#                                 Q(patient_national_id__icontains=value)
#                                 )
#     return render(request,  'accounts_app/partials/table_patients.html', {'patient': patient})

def search_patient(request):
    user = request.user.id
    value = request.GET.get('q_patient', '').strip()
    if not value:
        return redirect('accounts:patients')
    
    try:
        patient = Patient.objects.filter(
            Q(is_active=True) & 
            Q(dentist=user) & (
                Q(name__icontains=value) | 
                Q(family__icontains=value) | 
                Q(phone_number__icontains=value) | 
                Q(patient_national_id__icontains=value)
            )
        )
    except Patient.DoesNotExist:
        return render(request, 'accounts_app/partials/patients.html', {'patients': None})  # Handle not found error gracefully

    # Do not print sensitive patient information
    return render(request, 'accounts_app/partials/patients.html', {'patients': patient})


class SearchBlogView(View):
    template_name = 'diseases_app/search_blog.html'
    def get(self, request):
        value = request.GET.get('q_blog').strip()
        try:
            diseases = Disease.objects.filter(
                Q(is_active=True) & (
                    Q(title__icontains=value)
                )
            )
        except Disease.DoesNotExist:
            return render(request, self.template_name, {'diseases': None})
        
        return render(request, self.template_name, {'diseases': diseases})
