from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Patient
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin', 'family')
    
    fieldsets = (       # UserChangeForm مربوط به 
        (None, {
            "fields": (
                'mobile_number', 'password')}),
        ('personal info', {
            'fields': ('email', 'name', 'family', 'gender', 'active_code')}),
        ('Permissions', {
            'fields': ('is_active', 'is_admin' , 'groups', 'user_permissions')}),
        )
    
    add_fieldsets = (       # UserCreationForm مربوط به 
        (None, {'fields': ('mobile_number', 'email', 'name', 'family', 'gender', 'password1', 'password2')}),
        )
    
    search_fields = ('mobile_number',)
    ordering = ('mobile_number',)
    filter_horizontal = ( 'groups', 'user_permissions')
    
# admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Patient)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'family', 'phone_number']