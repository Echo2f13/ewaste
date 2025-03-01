from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib import messages
from events.models import userFull
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse

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
                return redirect("home", pk=user.id)
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

def profile(request, pk):
    user = request.user
    try:
        profile = userFull.objects.get(user=user)
    except userFull.DoesNotExist:
        profile = None  # Handle missing profile

    return render(request, "base/profile.html", {"user": user, "profile": profile})

def home(request,pk):
    return render(request, 'base/home.html')

def sell(request,pk):
    return render(request, 'base/sell.html')
from django.contrib.auth import update_session_auth_hash

@login_required
def change_address(request):
    if request.method == "POST":
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("country")

        profile, _ = userFull.objects.update_or_create(
            user=request.user,
            defaults={
                "userFull_street": street,
                "userFull_city": city,
                "userFull_state": state,
                "userFull_zipcode": zipcode,
                "userFull_country": country,
            },
        )

        messages.success(request, "Address updated successfully!")
        return redirect("profile", pk=request.user.pk)  # Ensure profile URL takes `pk`

    return redirect("profile", pk=request.user.pk)  # No separate page, go to profile

@login_required
def change_password(request):
    user = request.user
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not user.check_password(old_password):
            return JsonResponse({"status": "error", "message": "Old password is incorrect!"})

        if new_password != confirm_password:
            return JsonResponse({"status": "error", "message": "New passwords do not match!"})

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keep user logged in

        return JsonResponse({"status": "success", "message": "Password changed successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request!"})

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Account deleted successfully!")
        return redirect("Index")  # Ensure 'home' is a valid URL

    return redirect("profile", pk=request.user.pk)  # Redirect to profile if not POST
