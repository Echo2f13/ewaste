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


def delivery_more_jobs(request, pk):
    delivery_guy = get_object_or_404(deliveryGuy, pk=pk)
    return render(request, "delivery/home.html", {"phone_number": delivery_guy.deliveryGuy_phoneNumber})

@login_required
def delivery_update_password(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('delivery_update_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('delivery_update_password')

        user.set_password(new_password)
        user.save()

        # ✅ This keeps the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")

        # Fetch delivery guy's primary key (pk)
        delivery_guy = deliveryGuy.objects.get(deliveryGuy_user=user)
        return redirect(reverse('delivery_more_jobs', kwargs={'pk': delivery_guy.pk}))

    return redirect('delivery_more_jobs')

@login_required
def delivery_update_phone(request):
    if request.method == "POST":
        new_phone = request.POST["new_phone"]

        # Check if the phone number already exists
        if deliveryGuy.objects.filter(deliveryGuy_phoneNumber=new_phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect('delivery_update_phone')

        delivery_guy = deliveryGuy.objects.get(deliveryGuy_user=request.user)
        delivery_guy.deliveryGuy_phoneNumber = new_phone
        delivery_guy.save()

        messages.success(request, "Phone number updated successfully.")

        # Ensure the redirect includes the required pk
        return redirect(reverse('delivery_more_jobs', kwargs={'pk': delivery_guy.pk}))

    return redirect('delivery_more_jobs')

