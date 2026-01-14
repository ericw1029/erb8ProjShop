from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
#from contacts.models import Contact

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
            return redirect('pages:index')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('accounts:login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('pages:index')
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

def dashboard(request):
    user_contacts = Contact.objects.all().filter(user_id=request.user.id).order_by('-contact_date')
    context = {
        "contacts" : user_contacts        
    }
    return render(request,'accounts/dashboard.html',context)

def password_reset(request):
    print("password_reset")
    return redirect('pages:index')
