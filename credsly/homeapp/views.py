from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
import data_analysis

User=get_user_model()
import uuid

# Create your views here.
def index(request):
    return render(request,'index.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:    
        return render(request,'sign-in.html')

def loginuser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user =User.objects.get(email=email)
        print(user)
        user = authenticate(request, username=user, password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, f'Wrong Email or Password')
            return redirect('signin')
    else:
        messages.error(request, f'BAD Request')
        return redirect('signin')




def signup(request):
    return render(request,'sign-up.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        username = uuid.uuid4()
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        ##################################################################
        messages.success(request, f'Your account has been created ! You are now able to log in')
        return redirect('signin')
    else:
        messages.error(request, f'BAD Request')
        return redirect('signup')

def dashboard(request):
    if(request.user.is_authenticated):
        user_details=User.objects.get(username=request.user)
        return render(request,'dashboard.html',{"userDetails" : user_details})
    return redirect('signin')    

def privacy(request):
    return render(request,'privacy_policy.html')    

def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signin')
    else:
        return redirect('signin')  

     
def uploadFacebookZip(request):
        if request.method == 'POST' and request.user.is_authenticated: 
            fs= FileSystemStorage() 
            fs.save(str(request.user.username)+"-facebook.zip",request.FILES['fbzip'])
            userdata = User.objects.get(username=request.user)
            userdata.facebook_zipname=userdata.username+"-facebook.zip"
            userdata.save()
            messages.success(request, f'File uploaded Successfully')
            return redirect('dashboard')
        else:
            messages.error(request, f'BAD Request')
            return redirect('dashboard')   

def uploadLinkedinZip(request):
        if request.method == 'POST' and request.user.is_authenticated: 
            fs= FileSystemStorage() 
            fs.save(str(request.user.username)+"-linkedin.zip",request.FILES['linkedinzip'])
            userdata = User.objects.get(username=request.user)
            userdata.linkedin_zipname=userdata.username+"-linkedin.zip"
            userdata.save()
            messages.success(request, f'File uploaded Successfully')
            return redirect('dashboard')
        else:
            messages.error(request, f'BAD Request')
            return redirect('dashboard')   

def uploadTwitterUsername(request):
        if request.method == 'POST' and request.user.is_authenticated: 
            username = request.POST['twitter_username']
            if username is not None or username !="":
                userdata = User.objects.get(username=request.user)
                userdata.twitter_username=username
                userdata.save()
                messages.success(request, f'File uploaded Successfully')
                return redirect('dashboard')
            else:
                messages.error(request, f'Please Enter Twitter Username')
                return redirect('dashboard')
        else:
            messages.error(request, f'BAD Request')
            return redirect('dashboard')                            

def get_credit_score(request):
    if request.user.is_authenticated:
        userdata = User.objects.get(username=request.user)
        if(userdata.twitter_username==None or userdata.facebook_zipname==None or userdata.linkedin_zipname==None):
            messages.error(request, f'Please upload all data to proceed')
            return redirect('dashboard')
        credit_score,total_credit,total_posts,total_likes,fb_comments,total_connections =  data_analysis.generate_credit_score(userdata.username, userdata.twitter_username,userdata.facebook_zipname,userdata.linkedin_zipname)  
        userdata.credit_score=credit_score
        userdata.total_posts=total_posts
        userdata.total_likes=total_likes
        userdata.total_friends=total_connections
        userdata.total_comments=fb_comments
        userdata.total_credit=total_credit
        userdata.save()
        return redirect('dashboard')

    else:
        messages.error(request, f'BAD Request')
        return redirect('dashboard')    
