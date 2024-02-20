from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
# Create your views here.
def index(request):
   return render(request, 'index.html')

def campaign(request):
    return render(request, 'campaign.html')
def about(request):
    return render(request, 'about.html')
def login(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')
def contact(request):
    return render(request, 'contact.html')
# def hawa(request,hawa):
#     return render(request, 'case_no_404.html')

