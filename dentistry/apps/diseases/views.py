from django.shortcuts import render
from .models import Disease
from django.views import View
# Create your views here.

class BlogView(View):
    def get(self, request, *args, **kwargs):
        diseases = Disease.objects.filter(is_active=True).order_by('-is_priority')
        last_diseases = Disease.objects.filter(is_active=True).order_by('-publication_date')[:3]
        return render(request, 'diseases_app/blag.html', {'diseases': diseases, 'last_diseases':last_diseases})