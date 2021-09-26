from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    return render(request,'index.html')

def sigin(request):
    return render(request,'sign-in.html')

def signup(request):
    return render(request,'sign-up.html')

def dashboard(request):
    return render(request,'dashboard.html')

def privacy(request):
    return render(request,'privacy_policy.html')    