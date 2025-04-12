from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from bmstu.models import *
from datetime import datetime, timedelta
import time


@login_required
def home(request):
    users = UserProfile.objects.all().order_by('username')
    return render(request, 'bmstu/home.html', {'users': users})


@login_required
def homeworks(request):
    if request.method == 'POST':
        last_upload_time = request.session.get('last_upload_time')
        current_time = time.time()
        
        if last_upload_time and current_time - float(last_upload_time) < 30:
            remaining_time = int(30 - (current_time - float(last_upload_time)))
            messages.error(request, f'Пожалуйста, подождите {remaining_time} секунд перед следующей загрузкой')
            return redirect('bmstu:homework')
            
        try:
            subject = Subject.objects.get(id=request.POST.get('subject'))
            title = request.POST.get('title')
            description = request.POST.get('description')
            file = request.FILES.get('file')
            
            if len(description) > 30:
                messages.error(request, 'Описание не должно превышать 50 символов')
                return redirect('bmstu:homework')

            homework = Homework.objects.create(
                title=title,
                description=description,
                file=file,
                subject=subject,
                student=request.user
            )
            
            request.session['last_upload_time'] = str(current_time)
            messages.success(request, 'Домашнее задание успешно загружено!')
            return redirect('bmstu:homework')
            
        except Subject.DoesNotExist:
            messages.error(request, 'Выбранный предмет не существует!')
        except Exception as e:
            messages.error(request, 'Произошла ошибка при загрузке домашнего задания!')
            return redirect('bmstu:homework')
    
    homeworks = Homework.objects.all().order_by('-uploaded_at')
    subjects = Subject.objects.all()
    
   
    for homework in homeworks:
        homework.votes = homework.get_votes_count()
        homework.user_vote = Vote.objects.filter(user=request.user, homework=homework).first()
    
    last_upload_time = request.session.get('last_upload_time')
    upload_disabled = False
    remaining_time = 0
    
    if last_upload_time:
        current_time = time.time()
        time_passed = current_time - float(last_upload_time)
        if time_passed < 30:
            upload_disabled = True
            remaining_time = int(30 - time_passed)
    
    context = {
        'homeworks': homeworks,
        'subjects': subjects,
        'upload_disabled': upload_disabled,
        'remaining_time': remaining_time
    }
    return render(request, 'bmstu/homework.html', context)


@login_required
def lecture(request):
    if request.method == 'POST':
        last_upload_time = request.session.get('last_upload_time_lecture')
        current_time = time.time()
        
        if last_upload_time and current_time - float(last_upload_time) < 30:
            remaining_time = int(30 - (current_time - float(last_upload_time)))
            messages.error(request, f'Пожалуйста, подождите {remaining_time} секунд перед следующей загрузкой')
            return redirect('bmstu:lecture')
            
        try:
            subject = Subject.objects.get(id=request.POST.get('subject'))
            title = request.POST.get('title')
            description = request.POST.get('description')
            file = request.FILES.get('file')
            
            if len(description) > 30:
                messages.error(request, 'Описание не должно превышать 50 символов')
                return redirect('bmstu:lecture')


            lecture = Lecture.objects.create(
                title=title,
                description=description,
                file=file,
                subject=subject,
                author=request.user
            )
            
            request.session['last_upload_time_lecture'] = str(current_time)
            messages.success(request, 'Лекция успешно загружена!')
            return redirect('bmstu:lecture')
            
        except Subject.DoesNotExist:
            messages.error(request, 'Выбранный предмет не существует!')
        except Exception as e:
            messages.error(request, 'Произошла ошибка при загрузке лекции!')
            return redirect('bmstu:lecture')
    
    lectures = Lecture.objects.all().order_by('-uploaded_at')
    subjects = Subject.objects.all()
    
  
    for lecture in lectures:
        lecture.votes = lecture.get_votes_count()
        lecture.user_vote = Vote.objects.filter(user=request.user, lecture=lecture).first()
    
    last_upload_time = request.session.get('last_upload_time_lecture')
    upload_disabled = False
    remaining_time = 0
    
    if last_upload_time:
        current_time = time.time()
        time_passed = current_time - float(last_upload_time)
        if time_passed < 30:
            upload_disabled = True
            remaining_time = int(30 - time_passed)
    
    context = {
        'lectures': lectures,
        'subjects': subjects,
        'upload_disabled': upload_disabled,
        'remaining_time': remaining_time
    }
    return render(request, 'bmstu/lecture.html', context)


@login_required
def stata(request):
    users = UserProfile.objects.all()
    user_stats = []
    
    for user in users:
        approved_homeworks = Homework.objects.filter(student=user, status='approved').count()
        approved_lectures = Lecture.objects.filter(author=user, status='approved').count()
        
        user_stats.append({
            'user': user,
            'homeworks_count': approved_homeworks,
            'lectures_count': approved_lectures,
            'total_count': approved_homeworks + approved_lectures
        })
    
   
    user_stats.sort(key=lambda x: x['total_count'], reverse=True)
    
    context = {
        'user_stats': user_stats,
    }
    return render(request, 'bmstu/stats.html', context)


def balance(request):
    balance, created = Balance.objects.get_or_create(user=request.user, defaults={'coins': 0})
    
    approved_homeworks = Homework.objects.filter(student=request.user, status='approved')
    approved_lectures = Lecture.objects.filter(author=request.user, status='approved')
    rejected_homework = Homework.objects.filter(student=request.user, status='rejected')
    rejected_lectures = Lecture.objects.filter(author=request.user, status='rejected')
    
    if request.user.username == 'admin':
        balance.coins = 999999
    else:
    
        balance.coins = (approved_homeworks.count() + approved_lectures.count()) * 10
        balance.coins -= (rejected_homework.count() + rejected_lectures.count())
    
    balance.save()
    
    user_money = {
        'user': request.user,
        'balance': balance.coins,
        'homeworks_count': approved_homeworks.count(), 
        'lectures_count': approved_lectures.count()
    }
    
    context = {
        'user_money': [user_money],
    }
    
    return render(request, 'bmstu/balance.html', context)


@login_required
def vote_homework(request, homework_id):
    if request.method == 'POST':
        homework = get_object_or_404(Homework, id=homework_id)
        is_like = request.POST.get('is_like') == 'true'
        
        
        vote = Vote.objects.filter(user=request.user, homework=homework).first()
        
        if vote:
            if vote.is_like == is_like:
           
                vote.delete()
                homework.update_status()
                votes = homework.get_votes_count()
                return JsonResponse({'status': 'removed', 'votes': votes})
            else:
        
                vote.is_like = is_like
                vote.save()
        else:
      
            Vote.objects.create(
                user=request.user,
                homework=homework,
                is_like=is_like
            )
        
        homework.update_status()
        votes = homework.get_votes_count()
        return JsonResponse({'status': 'success', 'votes': votes})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def vote_lecture(request, lecture_id):
    if request.method == 'POST':
        lecture = get_object_or_404(Lecture, id=lecture_id)
        is_like = request.POST.get('is_like') == 'true'
        
     
        vote = Vote.objects.filter(user=request.user, lecture=lecture).first()
        
        if vote:
            if vote.is_like == is_like:
               
                vote.delete()
                lecture.update_status()
                votes = lecture.get_votes_count()
                return JsonResponse({'status': 'removed', 'votes': votes})
            else:
           
                vote.is_like = is_like
                vote.save()
        else:
           
            Vote.objects.create(
                user=request.user,
                lecture=lecture,
                is_like=is_like
            )
        
        lecture.update_status()
        votes = lecture.get_votes_count()
        return JsonResponse({'status': 'success', 'votes': votes})
    
    return JsonResponse({'status': 'error'}, status=400)
        