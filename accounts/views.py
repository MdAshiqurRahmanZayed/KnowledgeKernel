from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators  import login_required
from .forms import RegistrationForm,UserProfileForm,UserCreateProfileForm
from .models import Account,UserProfile
from django.contrib import messages
from courses.models import Course,EnrolledCourse
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
#register
def register(request):
     if request.method == "POST":
          try:
               form = RegistrationForm(request.POST)
               # user_test = Account.objects.filter(email=email).exists()
               # print(form)
               if form.is_valid():
                         email = form.cleaned_data['email']
                         password = form.cleaned_data['password']
                         username = email.split("@")[0]
                              
                         user = Account.objects.create_user( email=email, username=username, password=password)
                         # user.is_active = True
                         if 'nstu' in email:
                              user.is_student = True
                         else:
                              user.is_instructor = True
                         user.save()
                         # USER ACTIVATION
                         current_site = get_current_site(request)
                         mail_subject = "Please activate your mail"
                         message = render_to_string('accounts/verifyByMail/account_verification_email.html',{
                              'user' :user,
                              'domain': current_site,
                              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                              'token':default_token_generator.make_token(user),
                         })
                         to_email = email
                         send_email = EmailMessage(mail_subject,message,to = [to_email]) 
                         send_email.send()
                         
                         messages.success(request,'Registration Successfull.Please activate your account ')
                         
                         return redirect('login')
          except:
                         messages.warning(request,'Check email and password')
                         return redirect('register')
     else:
          form =  RegistrationForm()
          
     
     context = {
          'form':form
     }
     
     return render(request,'accounts/register.html',context)


def activate(request,uidb64,token):
     try:
          uid = urlsafe_base64_decode(uidb64).decode()
          user = Account._default_manager.get(pk=uid)
     except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
          user=None
     if user is not None and default_token_generator.check_token(user, token):
          user.is_active = True
          user.save()
          messages.success(request, 'Congratulations! Your account is activated.')
          return redirect('login')
     else:
          messages.error(request, 'Invalid activation link')
          return redirect('register')
     

#login
def login(request):
     if request.method == "POST":
          email = request.POST['email']
          password = request.POST['password']
          user = auth.authenticate( email=email, password=password)
          if user is not None:
               auth.login(request,user)
               messages.success(request, 'You are successfully logged in.')
               return redirect('dashboard')
          else:
               messages.warning(request, 'Bad cradentials.')
               return redirect('login')
          
     return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
     auth.logout(request)
     messages.success(request, 'You are logged out.')
     return redirect('login')

@login_required(login_url='login')
def dashboard(request):
     
     if UserProfile.objects.filter(user__id = request.user.id).exists():
          userprofile = UserProfile.objects.get(user = request.user)
          createdCourse = Course.objects.filter(instructor = userprofile).count()
          enrolled_course = EnrolledCourse.objects.filter(user = request.user).count()
     else:
          userprofile = "Please Complete Your Profile"
          createdCourse = "0"
          enrolled_course = EnrolledCourse.objects.filter(user = request.user).count()
          
     context = {
          'userprofile':userprofile,
          'createdCourse':createdCourse,
          'enrolled_course':enrolled_course,
     } 
     
     return render(request,'accounts/dashboard.html',context)



@login_required(login_url='login')
def create_profile(request):
     if UserProfile.objects.filter(user__email = request.user.email).exists():
          messages.warning(request,"Already created Profile")
          return redirect('dashboard')
     else:
          
          if request.method == "POST":
               profile_form = UserCreateProfileForm(request.POST  ,  request.FILES)
               user = request.user
               if profile_form.is_valid():
                    
                    profile =  profile_form.save( commit=False)
                    profile.user = user
                    profile.save()  
                    
                    messages.success(request, 'Your profile has been created successfully.')
                    return redirect('edit_profile')
          else:
               profile_form = UserCreateProfileForm()
          context = {
               'profile_form':profile_form
          }
     return render(request,'accounts/create_profile.html',context)
               






@login_required(login_url='login')
def editProfile(request):
     userprofile = get_object_or_404(UserProfile, user=request.user)
     if request.method == "POST":
          profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
          if profile_form.is_valid():
               profile_form.save()
               messages.success(request, 'Your profile has been updated successfully.')
               return redirect('edit_profile')
     else:
          profile_form = UserProfileForm(instance=userprofile)
     context = {
          'userprofile':userprofile,
          'profile_form':profile_form
     }
     return render(request,'accounts/edit-profile.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.warning(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.warning(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

