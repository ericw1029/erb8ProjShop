from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User
#from contacts.models import Contact

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from .forms import CustomPasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from .forms import ProfileForm

from urllib.parse import urlencode
from django.urls import reverse

# Create your views here.
def login(request):
    if request.method == "POST":
        #Handle login here
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Your are now logged in")
            #return redirect('accounts:dashboard')
            return redirect("pages:product_list")
        else:
            messages.error(request,"Invalid credentials")
            return redirect('accounts:login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('pages:product_list')
    #return render(request,'accounts/logout.html')

def register(request):
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists')
                return redirect('accounts:register')
            else: 
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already exists')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                    user.save()
                    messages.error(request,'Your are now registered and can log in')
                    return redirect('accounts:login')
        else:
            messages.error(request,'Passwods do not match')
            return redirect('accounts:register')
    else:
        return render(request,'accounts/register.html')

# def dashboard(request):
#     user_contacts = Contact.objects.all().filter(user_id=request.user.id).order_by('-contact_date')
#     context = {
#         "contacts" : user_contacts        
#     }
#     return render(request,'accounts/dashboard.html',context)

# def dashboard(request):
    
#     return redirect("pages/product_list.html")

def password_reset_confirm(request):
    return render(request,'accounts/password_reset_confirm.html')

def password_reset_complete(request):
    return render(request,'accounts/password_reset_complete.html')

def password_reset_done(request):
    return render(request,'accounts/password_reset_done.html')

def password_change_done(request):
    return render(request,'accounts/password_change_done.html')

@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            # Change the password
            new_password = form.cleaned_data.get("new_password1")
            request.user.set_password(new_password)
            request.user.save()

            # Update session to prevent logout
            update_session_auth_hash(request, request.user)

            # Add success message
            messages.success(request, "Your password has been changed successfully!")

            # Redirect to profile or success page
            return redirect("accounts:change_password_done")  # Change to your desired redirect
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = {"form": form, "title": "Change Password"}
    return render(request, "accounts/change_password.html", context)

@login_required
def change_password_done(request):
    return render(request, "accounts/change_password_done.html")

# Password Reset Views (for forgotten passwords)
def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email__iexact=email)
            if associated_users.exists():
                for user in associated_users:
                    # Generate password reset token
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))

                    # Build reset URL
                    reset_url = request.build_absolute_uri(
                        reverse(
                            "accounts:reset_password_confirm",
                            kwargs={"uidb64": uid, "token": token},
                        )
                    )

                    # Email content
                    subject = "Password Reset Request"
                    message = render_to_string(
                        "accounts/reset_password_email.html",
                        {
                            "user": user,
                            "reset_url": reset_url,
                            "site_name": "Your Site Name",
                        },
                    )

                    # Send email
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

            # Always show success message (for security reasons)
            messages.success(
                request, "Password reset link has been sent to your email."
            )
            return redirect("accounts:reset_password_done")
    else:
        form = PasswordResetForm()

    return render(request, "accounts/reset_password.html", {"form": form})


def reset_password_done(request):
    return render(request, "accounts/reset_password_done.html")


def reset_password_confirm(request, uidb64=None, token=None):
    if request.method == "GET":
        # Verify token and show password reset form
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Token is valid, show password reset form
            form = SetPasswordForm(user)
            return render(
                request,
                "accounts/reset_password_confirm.html",
                {"form": form, "validlink": True},
            )
        else:
            # Invalid token
            return render(
                request, "accounts/reset_password_confirm.html", {"validlink": False}
            )

    elif request.method == "POST":
        # Process password reset form
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully!")
                return redirect("accounts:reset_password_complete")
            else:
                return render(
                    request,
                    "accounts/reset_password_confirm.html",
                    {"form": form, "validlink": True},
                )
        else:
            return render(
                request, "accounts/reset_password_confirm.html", {"validlink": False}
            )


def reset_password_complete(request):
    return render(request, "accounts/reset_password_complete.html")

@login_required
def profile(request):
    return render(request, "accounts/profile.html")

def profile_detail(request, pk):
    """View individual profile details"""
    profileExist = Profile.objects.filter(user_id=pk).exists()
    if profileExist:
        profile = get_object_or_404(Profile, user_id=pk)
        context = {"profile": profile}
        return render(request, "accounts/profile_detail.html", context)
    else:
        # Use reverse properly - no need to manually construct the URL
        # If profile_create expects a URL parameter, define it in urls.py
        # If it uses GET parameter (as in your code), just redirect to it
        return redirect(f"{reverse('accounts:profile_create')}?user_id={pk}")


# def edit_profile(request, pk):
#     """View individual profile details"""
#     print("edit_profile", pk)
#     current_user = User.objects.get(id=pk)
#     form = ProfileForm()
#     profileExist = Profile.objects.filter(pk=pk).exists()
#     # profile = get_object_or_404(Profile, pk=pk)
#     if profileExist:
#         context = {"profile": profile,"saveType":"update"}
#         return render(request, "accounts/profile_form.html", context)
#     else:      
#         print("edit_profile  none", profile)  
            
#         context = {"form": form, "current_user": current_user, "saveType": "create"}
#         print("edit_profile", context['saveType'])
#         return render(request, "accounts/profile_form.html", context)
def edit_profile(request, pk):
    """View individual profile details"""
    print("edit_profile", pk)
   
    profileExist = Profile.objects.filter(user_id=pk).exists()
    # profile = get_object_or_404(Profile, pk=pk)
    if profileExist:
        profile= Profile.objects.get(user_id=pk)
        # Fix: redirect() takes the URL as first argument, not request
        return redirect("accounts:profile_detail", pk=profile.id)
    else:
        # Use reverse properly - no need to manually construct the URL
        # If profile_create expects a URL parameter, define it in urls.py
        # If it uses GET parameter (as in your code), just redirect to it
        return redirect(f"{reverse('accounts:profile_create')}?user_id={pk}")


def profile_create(request,user_id=None):
    """Create a new profile"""
    # Access the parameters using request.GET    
    print("profile_create", user_id)    
    if request.method == "POST":
        print("POST data:", request.POST)  # Debug: see what's being submitted
        print("User ID:", request.POST['user_id'])  # Debug: check if user_id is correct
        current_user = User.objects.get(id=request.POST["user_id"])
        
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            # Set the user for the profile
            profile.user = current_user
            # Now save to database
            profile.save()
            messages.success(
                request, f"Profile for {profile.full_name()} created successfully!"
            )
            return redirect("accounts:profile_detail", pk=profile.user_id)
    else:
        user_id = request.GET.get("user_id")
        current_user = User.objects.get(id=user_id)
        initial_data = {
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
            "user": current_user,
        }
        form = ProfileForm(initial=initial_data)

    context = {"form": form, "title": "Create New Profile","user_id":user_id}
    return render(request, "accounts/profile_form.html", context)


def profile_update(request, pk):
    """Update an existing profile"""
    profile = get_object_or_404(Profile, user_id=pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Profile for {profile.full_name()} updated successfully!"
            )
            return redirect("accounts:profile_detail", pk=profile.user_id)
    else:
        form = ProfileForm(instance=profile)

    context = {"form": form, "profile": profile, "title": "Update Profile"}
    return render(request, "accounts/profile_form.html", context)