from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'base/login.html')

def signup(request):
    return render(request,'base/signup.html')