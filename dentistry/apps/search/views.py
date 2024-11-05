from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# def search_patient(request):
#     search_value = request.GET.get('val')
    
#     if search_value is None:
#         return HttpResponse("No search value provided.")

#     print(search_value + '*'*50)
#     return HttpResponse(search_value)


def search_patient(request):  
    res = request.GET.get('val')
    print(query + '*'*50)
    return HttpResponse(res)
