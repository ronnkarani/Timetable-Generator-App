from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import User, School

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def create_school_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        school_name = request.POST.get('school_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('create_school_admin')

        school, _ = School.objects.get_or_create(name=school_name)
        user = User.objects.create_user(
            username=username,
            password=password,
            role='admin',
            school=school
        )
        messages.success(request, f"Admin for {school_name} created successfully!")
        return redirect('dashboard')

    return render(request, 'accounts/create_school_admin.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
