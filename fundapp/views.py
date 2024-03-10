# Normal Djanngo imports
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal
# for login systems and user related systems
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
# for message display
from django.contrib import messages
# Models import
from .models import AllFund, EsewaClaim, KhaltiClaim, BankClaim, Transaction
from . models import Usermessage
# Payment Gateway API imports
# esewa
import uuid
import requests as req
import hmac
import hashlib
import base64
import json



# Create your views here.
def index(request):
   return render(request, 'index.html')

def campaign(request):
    allfund= AllFund.objects.all()[::-1]
    context = {"allfund": allfund}
    return render(request, 'campaign.html', context)
def search_campaigns(request):
    query = request.GET.get('q')
    if query:
        results =AllFund.objects.filter(title__icontains=query)
    else:
        results = []
    return render(request, 'search.html', {'results': results})
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
#for contact page
def contact(request):    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        contact = Usermessage(name=name,email=email,message=message)
        contact.save()
        messages.success(request, 'Your message has been successfully sent!')
    else:
        HttpResponseNotFound("Dont try to be cool")
    return render(request, 'contact.html')
        
        
        
@login_required(login_url='/login/')
def startfund(request):
    if request.method == 'POST':
        image = request.FILES['image']
        title = request.POST['title']
        description = request.POST['description']
        campaignType = request.POST['campaignType']
        requiredFund = request.POST['requiredFund']
        toSave = AllFund(user = request.user, image= image, title= title, description= description, campaignType= campaignType, required=requiredFund)
        toSave.save()
        message = "Sucessfully Started the Campaign"
        messages.success(request, message)
        return redirect('/campaign')
    return render(request, 'startfund.html')

def campaigndetails(request, slug):
    allfund = AllFund.objects.filter(slug=slug).first()
    context ={"allfund": allfund} 
    return render(request, 'campaigndetails.html', context)

@login_required(login_url='/login/')
def campaignstatus(request):
    myCampaigns = AllFund.objects.filter(user=request.user)
    context = {"myCampaigns": myCampaigns}
    return render(request, 'campaignStatus.html', context)

def fundclaiming(request,post_id):
    campaign = get_object_or_404(AllFund, sno=post_id, user=request.user)
    outercontext = {"campaign": campaign}
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'esewa':
            esewa_number = request.POST.get('esewanumber')
            esewa_address = request.POST.get('esewaaddress')
            esewaToSave = EsewaClaim(user = request.user ,phoneNumber = esewa_number, receivingAddress = esewa_address)
            esewaToSave.save()
            # To delete the campaign after saving details
            campaign.delete()
            messages.success(request, 'We will send you the amount, your campaign is removed sucessfully.')
            return redirect('/')
        elif form_type == 'khalti':
            khalti_number = request.POST.get('khaltinumber')
            khalti_address = request.POST.get('khaltiaddress')
            khaltiToSave = KhaltiClaim(user = request.user ,phoneNumber = khalti_number, receivingAddress = khalti_address)
            khaltiToSave.save()
            # To delete the campaign after saving details
            campaign.delete()
            messages.success(request, 'We will send you the amount, your campaign is removed sucessfully.')
            return redirect('/')

        elif form_type == 'bank':
            bankname = request.POST.get('bankname')
            accountname = request.POST.get('accountname')
            accountnumber = request.POST.get('accountnumber')
            receivingperson = request.POST.get('receivingperson')
            receivingaddress = request.POST.get('receivingaddress')
            receivingphone = request.POST.get('receivingphone')
            bankToSave = BankClaim(user = request.user ,bankName = bankname ,accountNumber=accountnumber,receivingName=receivingperson,accountName = accountname  ,receivingAddress=receivingaddress ,phoneNumber=receivingphone )
            bankToSave.save() 
            # To delete the campaign after saving details
            campaign.delete()
            messages.success(request, 'We will send you the amount, your campaign is removed sucessfully for now.')
            return redirect('/')           
    return render(request, 'fundclaiming.html', outercontext)


# For Payment Gateways
# for esewa
def esewasahayog(request, slug):
    allfund = AllFund.objects.filter(slug=slug).first()
    if request.method == "POST":
        amtt = request.POST["amount"]
        res = Decimal(amtt) # converting the amount into decimal value
            
        def genSha256(key, message):
            key = key.encode('utf-8')
            message = message.encode('utf-8')
            hmac_sha256 = hmac.new(key, message, hashlib.sha256)
            digest = hmac_sha256.digest()
            # Convert the digest to a Base64-encoded string
            signature = base64.b64encode(digest).decode('utf-8')
            return signature
        
        total_amount = res
        secret_key = "8gBm/:&EnhH.1/q"  #form esewa Docs
        uid= uuid.uuid4()
        data_to_sign = f"total_amount={total_amount},transaction_uuid={uid},product_code=EPAYTEST" #form esewa Docs and v2 requirements
        result = genSha256(secret_key, data_to_sign)
        
        context = {
            "res": res,
            'total_amount': total_amount,
            "allfund": allfund,
            'uid': uid,
            'signature': result
        }
        return render(request, "foresewa.html", context)
    
    outercontext = {"allfund": allfund}
    return render(request, "esewasahayog.html", outercontext)


def payment_is_successful(request, slug, res):
    # note: res is the total amount passed from 'esewasahayog.html' page
    allfund = AllFund.objects.filter(slug=slug).first()
    if request.method == "GET":
        try:
            data = request.GET.get('data')
            decoded_data = base64.b64decode(data).decode('utf-8')
            map_data = json.loads(decoded_data)         
            if(map_data.get('status') == 'COMPLETE'):
                
                transaction = Transaction(
                    user=request.user,
                    medium='Esewa', 
                    amount=res,
                    amountReceiver=allfund.user,
                    campaignTitle=allfund,
                )
                transaction.save()
                
                allfund.have += res
                allfund.save()
            messages.success(request, "Payment successful")
            return redirect("/") 
        except:
            return HttpResponseNotFound("Error.")
    return redirect("/")

# Delete Systems
# Own Campaign Delete System
@login_required(login_url='/login/')
def deleteCampaign(request,post_id):
    try:
        post = AllFund.objects.get(sno=post_id)
        post.delete()
        messages.success(request, "Deleted Campaign Successfully")
        return redirect('/')
    except AllFund.DoesNotExist:
        return HttpResponseNotFound("Post not found.")
    
#editCampaign
def editCampaign(request, post_id):
    campaign = get_object_or_404(AllFund, sno=post_id, user=request.user)
    context = {"campaign": campaign}
    return render(request, 'editCampaign.html', context)

# Update Systems
@login_required(login_url='/login/')
def updateCampaign(request, post_id):
    campaign = get_object_or_404(AllFund, sno=post_id, user=request.user)

    if request.method == 'POST':
        updatetitle = request.POST.get('updatetitle', '').strip()
        updatedescription = request.POST.get('updatedescription', '').strip()
        updateType = request.POST.get('updateType', '').strip()
        updaterequired = request.POST.get('updaterequired', '').strip()
        updateimage = request.FILES.get('updateimage')

        if updatetitle:
            campaign.title = updatetitle
        if updatedescription:
            campaign.description = updatedescription
        if updateType:
            campaign.campaignType = updateType
        if updaterequired:
            campaign.required = updaterequired
        if updateimage:
            campaign.image = updateimage
        campaign.save()
        messages.success(request, "Updated Campaign Successfully")
        return redirect('/')
    context = {'campaign': campaign}
    return render(request, 'editCampaign.html', context)
    
# def hawa(request,hawa):
#     return render(request, 'case_no_404.html')
