from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from events.models import userFull, product, cart, PRODUCT_CATEGORIES, userCredits
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt


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
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        print("first_name, last_name, username, email, password, phone_number")  
        print(first_name, last_name, username, email, password, phone_number)  

        if User.objects.filter(email=email).exists():
            print("email already exists")
            return render(request, "base/signup.html", {"message1": 1})

        try:
            print("trying")

            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                first_name=first_name,
                last_name=last_name,
            )

            # ✅ Create or get userFull profile
            new_user_full, created = userFull.objects.get_or_create(
                user=new_user, defaults={"userFull_phoneNumber": phone_number}
            )
            if created:
                print("✅ userFull profile created successfully!")
            else:
                print("⚠️ userFull profile already existed!")
            
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
    # Get the user using the pk
    user = get_object_or_404(User, pk=pk)

    # Try to get the profile related to the user
    try:
        profile = userFull.objects.get(user=user)
    except userFull.DoesNotExist:
        profile = None  # Handle missing profile gracefully

    return render(request, "base/profile.html", {"user": user, "profile": profile})

def home(request, pk):
    try:
        current_userFull = userFull.objects.get(user=pk)
    except userFull.DoesNotExist:
        current_userFull = None  # Set to None if the userFull entry is missing

    categories = product.objects.values_list('product_category', flat=True).distinct()

    categorized_products = {
        category: product.objects.filter(product_category=category)
        .exclude(product_seller=current_userFull)
        .exclude(product_sold=True)
        for category in categories
    } if current_userFull else {}  # Avoid filtering if userFull is missing

    user_products = product.objects.filter(product_seller=current_userFull) if current_userFull else []

    # ✅ Ensure userCredits exists
    user_credits, created = userCredits.objects.get_or_create(user_id=pk, defaults={"Credits": 0})

    return render(request, 'base/home.html', {
        'categorized_products': categorized_products,
        'user_products': user_products,
        'current_userFull': current_userFull,
        'user_credits': user_credits  # ✅ Now properly defined
    })






@login_required
def sell(request, pk):
    seller = get_object_or_404(userFull, user_id = pk)  # Fetch seller by pk
    print("Got into sell view - Method:", request.method)

    if request.method == "POST":
        print("Form submitted - POST data:", request.POST)
        print("FILES data:", request.FILES)

        product_category = request.POST.get("product_category")
        product_name = request.POST.get("product_name")
        product_description = request.POST.get("product_description")
        product_bought_price = request.POST.get("product_bought_price", 0)
        product_bought_date = request.POST.get("product_bought_date", None)
        product_discount = request.POST.get("product_discount", 0)
        product_sell_price = request.POST.get("product_sell_price", 0)

        # Handling images
        product_image_1 = request.FILES.get("product_image_1")
        product_image_2 = request.FILES.get("product_image_2")
        product_image_3 = request.FILES.get("product_image_3")
        product_image_4 = request.FILES.get("product_image_4")

        print(f"Image1: {product_image_1}, Discount: {product_discount}")

        # Create product instance
        new_product = product.objects.create(
            product_seller_id=seller.userFull_id,
            product_category=product_category,
            product_name=product_name,
            product_description=product_description,
            product_bought_price=int(product_bought_price),
            product_bought_date=product_bought_date,
            product_discount=int(product_discount),
            product_sell_price=int(product_sell_price),
            product_image_1=product_image_1,
            product_image_2=product_image_2,
            product_image_3=product_image_3,
            product_image_4=product_image_4,
        )

        print("Product successfully created:", new_product)
        messages.success(request, "Product added successfully!")

        return redirect("home", pk=pk)  # Redirect to home page

    print("Work not done - rendering sell page")
    return render(request, "base/sell.html", {"seller": seller, "product_categories": PRODUCT_CATEGORIES})

def product_detail(request, pk, pk2):
    current_userFull = userFull.objects.get(user=pk)
    product_obj = get_object_or_404(product, product_id=pk2)
    return render(request, 'base/product_detail.html', {'product': product_obj, 'user': current_userFull.user})

@login_required
def add_to_cart(request, pk, pk2):
    current_user = User.objects.get(id=pk)
    product_obj = get_object_or_404(product, product_id=pk2)

    cart_item, created = cart.objects.get_or_create(user=current_user, product=product_obj)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    product_obj.product_sold = True
    product_obj.save()
    return redirect("home", pk=pk)


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
 # Import userFull model

@login_required
def edit_profile(request):
    user = request.user
    profile, _ = userFull.objects.get_or_create(user=user)  # Fetch profile safely

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.username = request.POST.get('username', user.username)
        profile.userFull_phoneNumber = request.POST.get('phone_number', profile.userFull_phoneNumber)

        # ✅ Profile Image Upload Handling
        uploaded_image = request.FILES.get('userFull_image')
        if uploaded_image:
            profile.userFull_image = uploaded_image

        user.save()
        profile.save()

        return redirect('profile',pk=user.id)  # Ensure 'profile' is the correct URL

    return render(request, 'profile.html', {'user': user, 'profile': profile})

def buy_credits(request, pk):
    if request.user.pk != pk:
        return redirect('home', pk=request.user.pk)
 

    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        credits_amount = int(request.POST.get('creditsAmount', 0))
        user_credits, created = userCredits.objects.get_or_create(user=user)
        user_credits.Credits += credits_amount
        user_credits.save()

        # 🔥 Refresh user session to reflect new credit balance
        request.user.refresh_from_db()

    return redirect('home', pk=pk)# Redirect back to home

