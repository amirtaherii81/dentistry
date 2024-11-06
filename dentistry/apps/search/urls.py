from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('patient/', views.search_patient, name='patient'),
]
