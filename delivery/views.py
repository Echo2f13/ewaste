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
from geopy.geocoders import Nominatim
# Create your views here.


def get_location(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

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



def dlv_more_jobs(request, pk):
    has_job = deliveryGuy.objects.filter(currently_working=1, deliveryGuy_user_id=pk).exists()
    products = product.objects.filter(product_sold=0, product_onDelivery = 1) 
    return render(request, "delivery/more_jobs.html", {"products": products, "has_job": has_job})

def select_dlv_product(request, pk, prod):
    dlv_guy = deliveryGuy.objects.filter(currently_working=False, deliveryGuy_user_id=pk).first()

    if dlv_guy:
        current_product = get_object_or_404(product, product_id=prod)
        current_product.product_sold = 1
        current_product.save()
        
        # Assign the product to the delivery guy
        dlv_guy.current_product = current_product
        dlv_guy.currently_working = True
        dlv_guy.save()
        
        # Fetch the corresponding delivery job
        current_dlv_product = get_object_or_404(deliveryJob, deliveryJob_product=current_product)
        current_dlv_product.deliveryJob_deliveryGuy = dlv_guy
        current_dlv_product.deliveryJob_status = 1
        current_dlv_product.save()  # Save the updated job
        
    return redirect('current_dlv_job', pk=pk)


def current_dlv_job(request, pk):
    dlv_guy = deliveryGuy.objects.filter(currently_working=True, deliveryGuy_user_id=pk).first()

    if not dlv_guy or not dlv_guy.current_product:
        print("working no dlv guy")
        return render(request, "delivery/job.html", {"has_job": False})  # No active job

    # Fetch the active delivery job
    dlv_job = deliveryJob.objects.filter(deliveryJob_deliveryGuy=dlv_guy, deliveryJob_product=dlv_guy.current_product).first()

    if not dlv_job:
        print("working no dlv job")
        return render(request, "delivery/job.html", {"has_job": False})  # No active delivery job

    # Get product details
    current_product = dlv_job.deliveryJob_product

    # Get seller and buyer locations (handle cases where location fetching might fail)
# Construct full address for seller and buyer
    seller_address = f"{current_product.product_seller.userFull_street}, {current_product.product_seller.userFull_city}, {current_product.product_seller.userFull_state}, {current_product.product_seller.userFull_zipcode}, {current_product.product_seller.userFull_country}"
    buyer_address = f"{dlv_job.deliveryJob_buyer.userFull_street}, {dlv_job.deliveryJob_buyer.userFull_city}, {dlv_job.deliveryJob_buyer.userFull_state}, {dlv_job.deliveryJob_buyer.userFull_zipcode}, {dlv_job.deliveryJob_buyer.userFull_country}"

    # Fetch latitude and longitude using the complete address
    seller_location = get_location(seller_address) or (None, None)
    buyer_location = get_location(buyer_address) or (None, None)

    # Extract latitude and longitude values
    seller_lat, seller_long = seller_location
    buyer_lat, buyer_long = buyer_location
    context = {
        "product": current_product,
        "has_job": True,
        "seller_lat": seller_lat,
        "seller_long": seller_long,
        "buyer_lat": buyer_lat,
        "buyer_long": buyer_long,
        "deliveryJob_status" : dlv_job.deliveryJob_status
    }

    return render(request, "delivery/job.html", context)

def mark_parcel_taken(request, pk):
    dlv_job = get_object_or_404(deliveryJob, deliveryJob_deliveryGuy__deliveryGuy_user_id=pk, deliveryJob_status=1)
    
    dlv_job.deliveryJob_status = 2
    dlv_job.save()
    
    return redirect('current_dlv_job', pk=pk)

def complete_delivery(request, pk):
    dlv_job = get_object_or_404(deliveryJob, deliveryJob_deliveryGuy__deliveryGuy_user_id=pk, deliveryJob_status=2)
    
    dlv_job.deliveryJob_status = 3  # Mark as delivered
    dlv_job.save()
    
    # Reset delivery guy's current job
    dlv_guy = dlv_job.deliveryJob_deliveryGuy
    if dlv_guy:
        dlv_guy.current_product = None
        dlv_guy.currently_working = False
        dlv_guy.save()
    
    return redirect('current_dlv_job', pk=pk)

def delivery_history(request, pk):
    completed_jobs = deliveryJob.objects.filter(deliveryJob_deliveryGuy__deliveryGuy_user_id=pk, deliveryJob_status=3)

    return render(request, "delivery/history.html", {"completed_jobs": completed_jobs})


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

