from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from events.models import userFull, product, cart, PRODUCT_CATEGORIES, userCredits, evaluatorGuy
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def eval_home(request,pk):
     return render(request, 'eval/home.html')

def eval_loginForm(request):
     if request.method == "POST":
          email = request.POST.get("email")
          password = request.POST.get("password")

          try:
               user = User.objects.get(email=email)
               eval_user = evaluatorGuy.objects.get(evaluatorGuy_user_id=user)
          except User.DoesNotExist:
               return render(
                    request, "eval/login.html", {"incorrect": "Email not registered"}
               )

          authenticated_user = authenticate(username=user.username, password=password)

          if authenticated_user:
               if user.is_active and not user.is_staff and not user.is_superuser:
                    login(request, authenticated_user)
                    return redirect("eval_home", pk=user.id)
               else:
                    return render(
                         request,
                         "eval/login.html",
                         {"incorrect": "User not active or unauthorized"},
                    )
          else:
               return render(
                    request, "eval/login.html", {"incorrect": "Incorrect credentials"}
               )

     return render(request, "eval/login.html")

def eval_signup(request):
     if request.method == "POST":
          first_name = request.POST.get("first_name")
          last_name = request.POST.get("last_name")
          username = request.POST.get("username")
          email = request.POST.get("email")
          phone = request.POST.get("phone")
          password = request.POST.get("password")

          try:
               if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                         username=username,
                         email=email,
                         password=password,
                         is_active=True,  # Account inactive until verified
                         first_name=first_name,
                         last_name=last_name,
                    )
                    user.save()

                    # Save additional Customer Care data
                    care_data = evaluatorGuy.objects.create(
                         evaluatorGuy_phoneNumber=phone,
                         evaluatorGuy_user=user,
                    )
                    care_data.save()
                    # Redirect to login page with success message
                    return redirect('eval_loginForm')
               else:
                    # If email exists, return error message
                    message1 = "A user with this email already exists."
                    return render(request, "eval/signup.html", {"message1": message1})

          except IntegrityError:
               # Handle database-related errors
               message1 = "There was an error processing your request. Please try again."
               return render(request, "eval/signup.html", {"message1": message1})

     # Render the signup form if not a POST request
     return render(request, "eval/signup.html")

def eval_logout(request):
    logout(request)
    return redirect("eval_loginForm")
