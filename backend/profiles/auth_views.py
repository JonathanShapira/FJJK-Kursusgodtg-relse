from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def login_view(request):
    """
    Custom login view
    """
    if request.user.is_authenticated:
        # All users (including superusers) redirect to profile page
        return redirect('/profile/profile-page/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # All users (including superusers) redirect to profile page
            return redirect('/profile/profile-page/')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'registration/login.html')


def register_view(request):
    """
    Custom registration view
    """
    if request.user.is_authenticated:
        return redirect('/profile/profile-page/')
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            trainer_for = request.POST.get('trainer_for')
            reg_number = request.POST.get('reg_number')
            account_number = request.POST.get('account_number')
            
            # Check if passwords match
            if password1 != password2:
                return JsonResponse({'success': False, 'error': 'Passwords do not match'})
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists'})
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already exists'})
            
            # Validate required profile fields
            if not trainer_for or not reg_number or not account_number:
                return JsonResponse({'success': False, 'error': 'Alle profil felter er påkrævet'})
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile with the provided data
            UserProfile.objects.create(
                user=user,
                trainer_for=trainer_for,
                reg_number=reg_number,
                account_number=account_number
            )
            
            # Automatically log in the user
            login(request, user)
            
            return JsonResponse({'success': True, 'redirect': '/profile/profile-page/'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'registration/register.html')


def logout_view(request):
    """
    Custom logout view
    """
    logout(request)
    return redirect('/login/')


def home_view(request):
    """
    Home view - redirect to login or profile
    """
    if request.user.is_authenticated:
        # All users (including superusers) redirect to profile page
        return redirect('/profile/profile-page/')
    else:
        return redirect('/login/')


def admin_info_view(request):
    """
    Admin info page
    """
    return render(request, 'admin_info.html')
