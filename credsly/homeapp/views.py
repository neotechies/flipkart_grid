from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
User=get_user_model()
import uuid

# Create your views here.
def index(request):
    return render(request,'index.html')

def signin(request):
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
    print(request.user.is_authenticated)
    print(request.user)
    user_details=User.objects.filter(username=request.user).all()
    print(user_details)
    return render(request,'dashboard.html')

def privacy(request):
    return render(request,'privacy_policy.html')    