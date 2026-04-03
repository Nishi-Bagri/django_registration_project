from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser
from django.http import HttpResponse

def register(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email'].lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        age = request.POST['age']
        
        house_no = request.POST.get('house_no')
        street = request.POST.get('street')
        district = request.POST.get('district')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        

         # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Password does not match")
            return redirect('register')
    
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # Password length validation
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect('register')

        hashed_password = make_password(password)
        print("HASHED PASSWORD:", hashed_password)
        
        # Save user
        CustomUser.objects.create(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone,
            age=age,

            house_no=house_no,
            street=street,
            district=district,
            city=city,
            pincode=pincode,

            role = 'user'
        )

        messages.success(request, "Registration successful!")
        return redirect('register')

    return render(request, 'users/register.html')

def user_login(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        # Empty field validation
        if not email or not password:
            messages.error(request, "All fields are required")
            return redirect('login')
        
        # Check if user exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request,"Email not registered")
            return redirect('login')

        # Check password
        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['role'] = user.role


            messages.success(request, "Login successful")

            #Role Based Routing

            if user.role == "admin":
                return redirect('admin_dashboard')
            else:
                return redirect('blog_list')
        
        else:
            print("Password mismatch")
            messages.error(request,"Invalid password")
            return redirect('login')
    
    return render(request, 'users/login.html')

def profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')
    
    user = CustomUser.objects.get(id=user_id)

    return render(request, 'users/profile.html', {'user': user})

def logout_user(request):
    request.session.flush()
    return redirect('login')

def edit_profile(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.age = request.POST.get('age')
        user.address = request.POST.get('address')

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']

        user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, 'users/edit_profile.html', {'user': user})

def user_list(request):

    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(id=user_id)

    if user.role != 'admin':
        return HttpResponse("Access Denied")
    
    users = CustomUser.objects.all()

    return render(request, 'users/user_list.html', {'users':users})