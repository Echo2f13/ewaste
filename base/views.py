from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()
def signupForm(request):
    if request.user.is_authenticated:
        print("work 1")
        return redirect("Login")  

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print("first_name, last_name, username, email, password")  
        print(first_name, last_name, username, email, password)  


        if User.objects.filter(email=email).exists():
            return render(request, "base/signup.html", {"message1": 1})

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                first_name=first_name,
                last_name=last_name,
            )
            
            return redirect("Login")
        
        except IntegrityError:
            return render(
                request,
                "base/signup.html",
                {"integrityerror": "A user with that username already exists."},
            )

    return render(request, "base/signup.html")

def loginForm(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request, "base/login.html", {"incorrect": "Email not registered"}
            )

        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user:
            if user.is_active and not user.is_staff and not user.is_superuser:
                login(request, authenticated_user)
                return render(
                    request,
                    "base/home.html",
                    {
                        "user": user,
                    },
                )
            else:
                return render(
                    request,
                    "base/login.html",
                    {"incorrect": "User not active or unauthorized"},
                )
        else:
            return render(
                request, "base/login.html", {"incorrect": "Incorrect credentials"}
            )

    return render(request, "base/login.html")

def logout_view(request):
    logout(request)
    return redirect("Login")