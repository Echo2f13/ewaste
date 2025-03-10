from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from events.models import userFull, product, cart, PRODUCT_CATEGORIES, userCredits, deliveryGuy, deliveryJob
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
# Create your views here.




def dlv_home(request,pk):
    return render(request, 'delivery/home.html')
def dlv_signup(request):
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
                dlv_data = deliveryGuy.objects.create(
                        deliveryGuy_phoneNumber=phone,
                        deliveryGuy_user=user,
                )
                dlv_data.save()
                # Redirect to login page with success message
                return redirect('dlv_loginForm')
            else:
                # If email exists, return error message
                message1 = "A user with this email already exists."
                return render(request, "delivery/signup.html", {"message1": message1})

        except IntegrityError:
            # Handle database-related errors
            message1 = "There was an error processing your request. Please try again."
            return render(request, "delivery/signup.html", {"message1": message1})

    # Render the signup form if not a POST request
    return render(request, "delivery/signup.html")


def dlv_loginForm(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            dlv_user = deliveryGuy.objects.get(deliveryGuy_user_id=user)
            print("eval user exist and the id:", dlv_user)
        except User.DoesNotExist:
            return render(
                request, "delivery/login.html", {"incorrect": "Email not registered"}
            )

        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user:
            if user.is_active and not user.is_staff and not user.is_superuser:
                login(request, authenticated_user)
                return redirect("dlv_home", pk=user.id)
            else:
                return render(
                        request,
                        "delivery/login.html",
                        {"incorrect": "User not active or unauthorized"},
                )
        else:
            return render(
                request, "delivery/login.html", {"incorrect": "Incorrect credentials"}
            )

    return render(request, "delivery/login.html")

def dlv_logout(request):
    logout(request)
    return redirect("dlv_loginForm")

