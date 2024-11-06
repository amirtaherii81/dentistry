from django.urls import path
from . import views

app_name = 'diseases'
urlpatterns = [
    path('', views.BlogView.as_view(), name='blog')
]
