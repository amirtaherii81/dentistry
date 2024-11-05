from django.contrib import admin
from .models import Disease
# Register your models here.

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'is_priority','is_active','publication_date']
    list_filter = ['title', 'is_priority', 'is_active']
    search_fields = ('title',)
    ordering = ('publication_date',)