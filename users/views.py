from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from users.models import UserProfile
from bmstu.models import Homework, Lecture


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        if 'avatar' in request.FILES:
            profile = user.profile
            profile.avatar = request.FILES['avatar']
            profile.save()
        
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('users:profile')
        
    return render(request, 'users/profile.html', {
        'user': request.user,
        'is_owner': True,
        'homeworks': Homework.objects.filter(student=request.user).order_by('-uploaded_at'),
        'lectures': Lecture.objects.filter(author=request.user).order_by('-uploaded_at')
    })


def view_profile(request, user_id):
    viewed_user = get_object_or_404(User, id=user_id)
    if viewed_user == request.user:
        return redirect('users:profile')
    return render(request, 'users/profile.html', {
        'user': viewed_user,
        'is_owner': False,
        'homeworks': Homework.objects.filter(student=viewed_user).order_by('-uploaded_at'),
        'lectures': Lecture.objects.filter(author=viewed_user).order_by('-uploaded_at')
    })


def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'users/login.html', {'error': 'Пользователь не найден'})
        auth.login(request,user)
        return HttpResponseRedirect(reverse('bmstu:home') + '?login_success=true')


def signup(request):
    if request.method == 'GET':
        return render(request, 'users/registration.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        email = request.POST['email']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                
                return redirect('users:login')
            except IntegrityError:
                return render(request, 'users/registration.html', {'error': 'Имя занято'})
        else:
            return render(request, 'users/registration.html', {'error': 'Пароли не совпадают'})
        
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('bmstu:home')

