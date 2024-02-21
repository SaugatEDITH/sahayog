# Normal Djanngo imports
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseNotFound
# for login systems and user related systems
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# for message display
from django.contrib import messages
# Models import
from .models import AllFund
# Payment Gateway API imports



# Create your views here.
def index(request):
   return render(request, 'index.html')

def campaign(request):
    allfund= AllFund.objects.all()
    context = {"allfund": allfund}
    return render(request, 'campaign.html', context)

def about(request):
    return render(request, 'about.html')

def handleSignup(request):
    """This functions handle all signup backend"""
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check for errors
        if len(username) > 10:
            messages.warning(
                request, "Username length must be less than 10 characters!")
            return redirect("/signup/")

        if not username.isalnum():
            messages.success(
                request, "Username should only contain letters and numbers!")
            return redirect("/signup/")

        if password != confirm_password:
            messages.error(request, "Password mismatch")
            return redirect("/signup/")

        # Create the user
        if(User.objects.filter(username = username)):
            messages.error(request, "Username already exists")
            return redirect('/signup/')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        messages.success(
            request, 'Your account has been successfully created!')
        print(f"Hello {username}")
        return redirect('/')
    if request.user.is_authenticated:
        return HttpResponse('$404- Don\'t try be cool!')
    else:
        return render(request, 'signup.html')

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginPassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginPassword)

        if user is not None:
            login(request, user)
            messages.success(
                request, "Sucessfully Logged in!")
            return redirect("/")  # redirect on home
        else:
            messages.error(
                request, "Invalid credentials, Please try again!")
            return redirect("/login/")  # redirect on home
    if request.user.is_authenticated:
        return HttpResponse('$404- Don\'t try be cool!')
    else:
        return render(request, 'login.html')

def handleLogout(request):
    logout(request)
    messages.success(
        request, "You are Logged Out!")
    return redirect("/")  # redirect on home

def contact(request):
    return render(request, 'contact.html')

# def hawa(request,hawa):
#     return render(request, 'case_no_404.html')