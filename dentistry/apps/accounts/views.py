from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (
    RegisterUserForm, LoginUserForm, PatientForm, EditeProfileForm,
    VerifyRegisterForm, RememberPasswordForm
    )
from .models import CustomUser, Patient
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from apps.diseases.models import Disease
import utils


class RegisterUserView(View):
    template_name = 'accounts_app/register.html'

    def get(self, request):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            active_code = utils.create_active_code(5)
            CustomUser.objects.create_user(
            name = data['name'],
            family = data['family'],
            mobile_number = data['mobile_number'],
            specialty = data['specialty'],
            password=data['password2'],
            active_code=active_code
            )
            utils.send_sms(data['mobile_number'], f'کد فعال سازی حساب کاربری شما {active_code} می باشد')
            request.session['user_session'] = {
                'active_code': str(active_code),
                'mobile_number': str(data['mobile_number']),
            }
            messages.success(request,'اطلاعات شما با موفقیت ثبت شد. کد دریافتی را وارد کنید', 'success')
            return redirect('accounts:verify')
        else:
            messages.error(request, "اطلاعات وارد شده معتبر نمی باشد", 'danger')
            return render(request, self.template_name, {"form": form})
        
#----------------------------------------------------------------
class VerifyUserView(View):
    template_name = 'accounts_app/verify_user.html'
    def get(self, request):
        form = VerifyRegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            remember_password = user_session.get('remember_password', False)
            if data['active_code'] == user_session['active_code']:
                if not remember_password:
                    user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                    user.is_active = True
                    user.active_code = utils.create_active_code(5)
                    user.save()
                    messages.success(request, 'ثبت نام شما با موفقیت انجام شد', 'success')
                    return redirect('accounts:login')
                else:
                    return redirect('accounts:change_password')
            else:
                messages.error(request, 'کد دریافتی اشتباه می باشد', 'danger')
        else:
            messages.error(request, 'اطلاعات وارد شده نامعتبر می باشند', 'danger')
        
        return render(request, self.template_name, {'form': form})

#---------------------------------------------------------------- 
class LoginUserView(View):
    template_name = 'accounts_app/login.html'

    def get(self, request):
        form = LoginUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['mobile_number'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود با موفقیت انجام شد', 'success')
                return redirect('accounts:user_panel')
            else:
                messages.warning(request, 'کاربر یافت نشد', 'warning')
                return render(request, self.template_name, {'form': form})
        else:
            messages.warning(request, "اطلاعات وارد شده معتبر نمیباشد", 'warning')

        return render(request, self.template_name, {'form': form})

#---------------------------------------------------------------]
class RememberPasswordView(View):
    template_name = 'accounts_app/partials/remember_password.html'
    def get(self, request):
        form = RememberPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code=utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data['mobile_number'], f'کد تایید حساب کاربری شما {active_code} می باشد')
                request.session['user_session'] = {
                    'active_code': str(active_code),
                    'mobile_number': str(data['mobile_number']),
                    'remember_password': True,
                }
                messages.success(request, 'جهت تغییر رمز عبور خود کد تایید را ارسال کنید', 'success')
                return redirect('accounts:verify')
            except:
                messages.error(request, 'شماره موبایل وارد شده موجود نمی باشد', 'danger')
                return render(request, self.template_name, {'form': form})
            
#----------------------------------------------------------------
class ChangePasswordView(View):
    template_name = 'accounts_app/partials/change_password.html'
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            user_session=request.session['user_session']
            user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code=utils.create_random_code(5)
            user.save()
            messages.success(request, 'رمز عبور شما با موفقعیت تغییر کرد', 'success')
            return redirect('accounts:login')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
        
        return render(request, self.template_name, {'form': form})

#----------------------------------------------------------------          
class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request,'خروج شما با موفقعیت انجام شد', 'success')
        return redirect('main:index')
    
#----------------------------------------------------------------          
class UserPanelView(View):
    template_name = 'accounts_app/userpanel.html'

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'لطفاً وارد شوید', 'danger')
            return redirect('accounts:login')
        dentist = CustomUser.objects.get(pk=request.user.id)
        return render(request, self.template_name, {'dentist': dentist})
    
    
#----------------------------------------------------------------          
class Patients(View):
    template_name = 'accounts_app/partials/patients.html'
    
    def get(self, request):
        patients = Patient.objects.filter(is_active=True, dentist=request.user.id)
        return render(request, self.template_name, {'patients': patients})

#----------------------------------------------------------------          
class EditProfileView(View):
    template_name = 'accounts_app/partials/edit_profile.html'
    def get(self, request):
        user = request.user
        data = {
            'mobile_number' : user.mobile_number,
            'name' : user.name,
            'family' : user.family,
            'specialty' : user.specialty,
        }
        
        form = EditeProfileForm(initial=data)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = EditeProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            user.mobile_number=data['mobile_number']
            user.name=data['name']
            user.family=data['family']
            user.email=data['email']
            user.specialty=data['specialty']
            user.save()
            messages.success(request, 'ویرایش پروفایل با موفقیت انجام شد', 'success')
            return redirect('accounts:user_panel')
        messages.error(request, 'اطلاعات وارد شده نامعتبراند', 'danger')
        return render(request, self.template_name, {'form': form})

#----------------------------------------------------------------          
class CreatePatient(View):
    template_name = 'accounts_app/partials/add_patient.html'
    def get(self, request):
        form = PatientForm()
        # diseases = Disease.objects.all().order_by('-is_priority')
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        user = CustomUser.objects.get(pk=request.user.id)
        form = PatientForm(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            patient = form.save(commit=False)  
            patient.dentist = request.user
            patient.save()

            # اضافه کردن بیماری‌ها  
            # diseases = request.POST.getlist('diseases')  # دریافت همه بیماری‌های انتخاب شده  
            # for disease_id in diseases:  
            #     disease = get_object_or_404(Disease, id=disease_id) 
            #     patient.diseases.add(disease)  # اضافه کردن بیماری به بیمار 
            messages.success(request, 'اطلاعات بیمار با موفقیت ثبت شد', 'success')
            return redirect('accounts:add_patients')
        else:
            print('*' * 50)
            print(form.errors)
            messages.error(request, 'اطلاعات وارد شده نامعتبراند', 'danger')
            return render(request, self.template_name, {'form': form})

#----------------------------------------------------------------          
class UpdatePatient(View):
    template_name = 'accounts_app/partials/edit_patient.html'
    def get(self, request, id):
        patient=Patient.objects.get(pk=id)
        all_diseases = Disease.objects.all()
        data = {
            'name': patient.name,
            'family': patient.family,
            'phone_number': patient.phone_number,
            'dentist': patient.dentist,
            'disease_ids': list( patient.diseases.all().values_list('id',flat=True)),
            'patient_national_id': patient.patient_national_id,
            'visit_date': patient.visit_date,
            'medical_history': patient.medical_history,
            'is_active': patient.is_active,
            'all_diseases':all_diseases
        }

        form = PatientForm(initial=data)
        return render(request, self.template_name, {'form': form, 'data': data})

