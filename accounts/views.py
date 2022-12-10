from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators  import login_required
from .forms import RegistrationForm,UserProfileForm,UserCreateProfileForm
from .models import Account,UserProfile
from django.contrib import messages
# Create your views here.

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
                         user.is_active = True
                         if 'nstu' in email:
                              user.is_student = True
                         else:
                              user.is_instructor = True
                         user.save()
                         messages.success(request,'Registration Successfull.Please Login.')
                         
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


#login
def login(request):
     if request.method == "POST":
          email = request.POST['email']
          password = request.POST['password']
          user = auth.authenticate( email=email, password=password)
          if user is not None:
               auth.login(request,user)
               return redirect('dashboard')
          else:
               return redirect('login')
          
     return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
     auth.logout(request)
     # messages.success(request, 'You are logged out.')
     return redirect('login')

@login_required(login_url='login')
def dashboard(request):
     if UserProfile.objects.filter(user = request.user).exists():
          userprofile = UserProfile.objects.get(user = request.user)
     else:
          userprofile = "Please Complete Your Profile"
     context = {
          'userprofile':userprofile
     } 
     
     return render(request,'accounts/dashboard.html',context)



@login_required(login_url='login')
def create_profile(request):
     
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
          profile_form = UserCreateProfileForm(request.POST or None)
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

