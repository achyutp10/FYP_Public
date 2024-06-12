from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from accounts.models import User, UserProfile
from technician.forms import TechnicianForm
from .forms import UserForm, UserProfileForm
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from technician.models import Technician
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

# Restrict the technician from accessing the customer page
def check_role_technician(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied


# Restrict the customer from accessing the technician page
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied
def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in!')
    return redirect('myAccount')
  elif request.method == 'POST':  
    form = UserForm(request.POST, request.FILES)
    if form.is_valid():
      # Create the user using the form
      # password = form.cleaned_data['password']
      # user = form.save(commit=False)
      # user.set_password(password)
      # user.role = User.CUSTOMER
      # user.save()

      #create user using the create_user method
      first_name = form.cleaned_data["first_name"]
      last_name = form.cleaned_data["last_name"]
      username = form.cleaned_data["username"]
      email = form.cleaned_data["email"]
      profile_picture = form.cleaned_data['profile_picture']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data["password"]
      user = User.objects.create_user(first_name=first_name,last_name=last_name, profile_picture=profile_picture, 
                                      email=email, phone_number=phone_number, username=username, password=password)
      user.role = User.CUSTOMER
      user.save()

      #Send verification email
      mail_subject = 'Please activate your account'
      email_template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request, user, mail_subject, email_template)
      messages.success(request, 'Your account has been registered successfully')
      return redirect('login')
    else:
      print('invalid form')
      print(form.errors)
  else:
    form = UserForm()
    
  context = {
    'form': form,
  }
  return render(request, 'accounts/registerUser.html', context)

# def registerTechnician(request):
#   if request.user.is_authenticated:
#     messages.warning(request, 'You are already logged in!')
#     return redirect('myAccount')  
#   elif request.method == 'POST':
#     #store the data and create the user
#     form = UserForm(request.POST)
#     t_form = TechnicianForm(request.POST, request.FILES)
#     if form.is_valid() and t_form.is_valid():
#       first_name = form.cleaned_data["first_name"]
#       last_name = form.cleaned_data["last_name"]
#       username = form.cleaned_data["username"]
#       email = form.cleaned_data["email"]
#       profile_picture = form.cleaned_data['profile_picture']
#       phone_number = form.cleaned_data['phone_number']
#       password = form.cleaned_data["password"]
#       user = User.objects.create_user(first_name=first_name,last_name=last_name, 
#                                       email=email, profile_picture=profile_picture, 
#                                       phone_number=phone_number, username=username, password=password)
#       user.role = User.TECHNICIAN
#       user.save()
#       technician = t_form.save(commit=False)
#       technician.user = user
#       user_profile = UserProfile.objects.get(user=user)
#       technician.user_profile = user_profile
#       technician.save()
#       messages.success(request, "Your account has been registered successfully")
#       return redirect('registerTechnician')  
#     else:
#       print('invalid form')
#       print(form.errors)  
#   else:  
#     form = UserForm()
#     t_form = TechnicianForm()
#   context = {
#     'form': form,
#     't_form': t_form,
#   }
#   return render(request, 'accounts/registerTechnician.html', context)

def registerTechnician(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')  
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        t_form = TechnicianForm(request.POST, request.FILES)
        if form.is_valid() and t_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            profile_picture = form.cleaned_data['profile_picture']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data["password"]
            
            # Check if 'profile_picture' is in request.FILES
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
            else:
                profile_picture = None

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, 
                username=username, password=password, profile_picture=profile_picture  # Passing the profile_picture
            )
            
            user.role = User.TECHNICIAN
            user.save()

            technician = t_form.save(commit=False)
            technician.user = user
            user_profile = UserProfile.objects.get(user=user)
            technician.user_profile = user_profile
            technician.save()

            # Saving the profile picture separately
            if profile_picture:
                user.profile_picture.save(profile_picture.name, profile_picture)

            #Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'

            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Your account has been registered successfully")
            return redirect('registerTechnician')  
        else:
            print('invalid form')
            print(form.errors)  
    else:  
        form = UserForm()
        t_form = TechnicianForm()
        
    context = {
        'form': form,
        't_form': t_form,
    }
    return render(request, 'accounts/registerTechnician.html', context)

def activate(request, uidb64, token):
  # Activate user by setting the is_active status to True
  try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
     user = None

  if user is not None and default_token_generator.check_token(user, token):
     user.is_active = True
     user.save()
     messages.success(request, 'Congratulations Your account is activated.')
     return redirect('myAccount')
  else:
     messages.error(request, 'The link was invalid or has expired.')
     return redirect('myAccount')

def login(request):
  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in!')
    return redirect('myAccount')
  elif request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)
    
    if user is not None:
      auth.login(request, user)
      if user.is_admin:
        return redirect('admin')
      else:
        messages.success(request, 'You are now logged in.')
        return redirect('home')
    else:
      messages.error(request, 'Invalid Login Credentials')
      return redirect('login')
      
  return render(request, 'accounts/login.html')


def logout(request):
  auth.logout(request)
  messages.info(request, 'You are logged out.')
  return redirect('login')

@login_required(login_url='login')
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    # Fetching all technician data here to display it in services
    all_technicians = Technician.objects.all()[1:3]
    
    context = {
        'all_technicians': all_technicians,
    }
    
    return render(request, 'accounts/custDashboard.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_technician)
def technicianDashboard(request):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    technician = get_object_or_404(Technician, user=request.user)

    if request.method == "POST":
       profile_form = UserProfileForm(request.POST, instance=profile)
       if profile_form.is_valid():
          profile_form.save()
          messages.success(request, 'Location Settings updated!')
          return redirect('technicianDashboard')
       else:
          print(profile_form.errors)

    else:
      profile_form = UserProfileForm(instance=profile)
    # Fetching all technician data here to display it in services
      technician = Technician.objects.get(user=request.user)
    
    context = {
        'technician': technician,
        'profile_form': profile_form,
    } 

    return render(request, 'accounts/technicianDashboard.html', context)

@login_required(login_url='login')
def updateTechnicianInfo(request):
  if request.method == 'POST':
      request.user.first_name = request.POST.get('first_name')
      request.user.last_name = request.POST.get('last_name')
      request.user.phone_number = request.POST.get('phone_number')
      request.user.save()

      technician = Technician.objects.get(user=request.user)
      technician.service_charge = request.POST.get('service_charge')
      technician.save()

      messages.success(request, 'Your profile has bees updated successfully')
      return redirect('technicianDashboard')
    
  return render(request, 'accounts/technicianDashboard.html')

@login_required(login_url='login')
def updateCustomerInfo(request):
  if request.method == 'POST':
      request.user.first_name = request.POST.get('first_name')
      request.user.last_name = request.POST.get('last_name')
      request.user.phone_number = request.POST.get('phone_number')
      request.user.save()

      messages.success(request, 'Your profile has bees updated successfully')
      return redirect('custDashboard')
    
  return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
def changePassTech(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # Check if the current password matches the user's password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('technicianDashboard')
        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('technicianDashboard')
        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()
        # Update session authentication hash to prevent logout
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password has been successfully updated.')
        return redirect('technicianDashboard')
    return render(request, 'accounts/technicianDashboard.html')

@login_required(login_url='login')
def changePassCust(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # Check if the current password matches the user's password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('custDashboard')

        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('custDashboard')
        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()
        # Update session authentication hash to prevent logout
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password has been successfully updated.')
        return redirect('custDashboard')
    return render(request, 'accounts/custDashboard.html')

def forgot_password(request):
   if request.method == 'POST':
      email = request.POST['email']
      if User.objects.filter(email=email).exists():
         user = User.objects.get(email__exact=email)
         # send reset password email
         mail_subject = 'Reset your password.'
         email_template = 'accounts/emails/reset_password_email.html'
         send_verification_email(request, user, mail_subject, email_template)

         messages.success(request, 'Password reset link has been sent to your email address')
         return redirect('login')
      else:
         messages.error(request, 'Account doesnot exist')
         return redirect('forgot_password')
   return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
  # validate user by decoding the token ad user pk
  try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
     user = None
  if user is not None and default_token_generator.check_token(user, token):
     request.session['uid']=uid
     messages.info(request, 'Please reset your password')
     return redirect('reset_password')
  else:
     messages.error(request, 'This link has been expired')
     return redirect('myAccount')

def reset_password(request):
   if request.method == 'POST':
      password = request.POST['password']
      confirm_password = request.POST['confirm_password']
      if password == confirm_password:
         pk = request.session.get('uid')
         user = User.objects.get(pk=pk)
         user.set_password(password)
         user.is_active = True
         user.save()
         messages.success(request, 'Password reset successfull')
         return redirect('login')
      else:
         messages.error(request,'Passwords do not match')
         return redirect('reset_password')
   return render(request, 'accounts/reset_password.html')

from django.shortcuts import get_object_or_404

def update_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        user_profile = request.user.userprofile  # Access UserProfile associated with current user
        technician = get_object_or_404(Technician, user_profile=user_profile)
        if status == 'Available':
            technician.is_available_status = True
            technician.save()
            messages.info(request, 'Availability status updated to Available.')
        elif status == 'Unavailable':
            technician.is_available_status = False
            technician.save()
            messages.info(request, 'Availability status updated to Unavailable.')
        return redirect('technicianDashboard')
    else:
        return render(request, 'accounts/technicianDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user
    if request.method == "POST":
       profile_form = UserProfileForm(request.POST, instance=profile)
       if profile_form.is_valid():
          profile_form.save()
          profile = profile_form.save(commit=False)
            # Update latitude and longitude from form data
          profile.latitude = request.POST.get('latitude')
          profile.longitude = request.POST.get('longitude')
          profile.save()
          messages.success(request, 'Location Settings updated!')
          return redirect('cprofile')
       else:
          print(profile_form.errors)
    else:
      profile_form = UserProfileForm(instance=profile)
    context = {
        'user': user,
        'profile_form': profile_form,
    } 
    return render(request, 'customer/cprofile.html', context)



